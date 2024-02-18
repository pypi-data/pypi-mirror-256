import os
import json
import logging
from functools import partial

import dash
import flask
import plotly
import pkgutil
import mimetypes
import dash_renderer
import dash_core_components as dcc

from dash.version import __version__
from dash._utils import (
    stringify_id,
    format_tag
)
from .utilities import is_authenticated
logger = logging.getLogger(__name__)
BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')

_app_entry = """
    <main id="AnalyticsAppsUI-container">
    </main>
"""

_report_content_entry_id_ = 'AnalyticsAppsUI-report-container'
_report_sidebar_entry_id_ = 'AnalyticsAppsUI-sidebar-container'

class OAPDash(dash.Dash):
    static_files = {
        'css': [
            'main.wrapper.css'
        ]
    }

    def __init__(self, **kwargs):
        self.route = kwargs.pop('route')
        app_id = os.getenv('APP_ID')
        self.in_store_id = "_oap_data_in_" + app_id
        self.out_store_id = "_oap_data_out_" + app_id

        route_prefix = f'/{self.route}' if self.route else ''
        # assume this is not set by user
        kwargs['requests_pathname_prefix'] = f'{route_prefix}/'

        super(OAPDash, self).__init__(**kwargs)

    def init_app(self, app=None):
        """
        called when the app is initiated, called only once
        register api endpoints and custom static resources
        """
        super(OAPDash, self).init_app(app)


        # register static files for wrapper
        self.server.register_blueprint(
            flask.Blueprint(
                'analytics_sdk_assets',
                self.config.name,
                static_url_path="{}{}".format(
                    self.config.routes_pathname_prefix,
                    'wrapper-static',
                    )
                )
            )

        # register manifest files
        self._add_url("opsramp-analytics-utils/<string:file_name>", self.serve_resource)
        self._add_url("asset-manifest.json", self.serve_manifest)


    def _index(self, *args, **kwargs):  # pylint: disable=unused-argument
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        metas = self._generate_meta_html()
        renderer = self._generate_renderer()

        # use self.title instead of app.config.title for backwards compatibility
        title = self.title

        if self._favicon:
            favicon_mod_time = os.path.getmtime(
                os.path.join(self.config.assets_folder, self._favicon)
            )
            favicon_url = self.get_asset_url(self._favicon) + "?m={}".format(
                favicon_mod_time
            )
        else:
            favicon_url = "{}_favicon.ico?v={}".format(
                self.config.requests_pathname_prefix, __version__
            )

        favicon = format_tag(
            "link",
            {"rel": "icon", "type": "image/x-icon", "href": favicon_url},
            opened=True,
        )

        index = self.interpolate_index(
            metas=metas,
            title=title,
            css=css,
            config=config,
            scripts=scripts,
            app_entry=_app_entry,
            favicon=favicon,
            renderer=renderer,
        )

        return index


    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        logger.info("verifying authentication")
        print("verifying authentication")
        if ('path' in kwargs and 'server/status' in kwargs['path'] ):
            logger.info("server is up and running")
            print("server is up and running")
            return 'server is up and running', 200
        elif is_authenticated():
            logger.info("authentication is successful")
            print("authentication is successful")
            resp = self._index(args, kwargs)
            return resp
        else:
            # return flask.Response('Not authorized', status=401)
            redirect_url = BASE_API_URL + f'/tenancy/web/login?cb=/loginResponse.do'
            logger.info("authentication is failed, redirecting to login url is %s", redirect_url)
            print("authentication is failed, redirecting to login url is ", redirect_url)
            return flask.redirect(redirect_url, code=302)


    def serve_manifest(self):
        return {
            "files": {
                "main.css": f"{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.css",
                "main.js": f"{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.js",
                # "main.js.map": "/analytics-apps/static/js/main.b42d7633.js.map",
                "index.html": f"{self.config.requests_pathname_prefix}index.html",
            },
            "entrypoints": [
                "main.css",
                "main.js"
            ]
        }

    def serve_resource(self, file_name):
        if file_name == 'main.css':
            return self._serve_main_css()
        elif file_name == 'main.js':
            return self._serve_main_js()
        elif file_name == 'report_main.js':
            return self._serve_report_main_js()
        else:
            extension = "." + file_name.split(".")[-1]
            mimetype = mimetypes.types_map.get(extension, "application/octet-stream")

            return flask.Response(
                pkgutil.get_data('dash_core_components', file_name), mimetype=mimetype
            )

    def _serve_main_css(self):
        body = ''

        # TODO: external css files using requests
        external_links = self.config.external_stylesheets

        # oap css files
        for file_path in self.static_files['css']:
            body += pkgutil.get_data('analytics_sdk', 'analysis-wrapper/'+file_path).decode("utf-8")
        body = body.replace('url(/static/media', f'url({self.config.requests_pathname_prefix}wrapper-static/media')

        # custom css files
        for resource in self.css.get_all_css():
            file_name = resource['asset_path']
            body += open(self.config.assets_folder+'/'+file_name).read()

        response = flask.Response(body, mimetype='text/css')

        return response

    def _serve_main_js(self):
        body = pkgutil.get_data('analytics_sdk', 'analysis-wrapper/main.js').decode("utf-8")
        response = flask.Response(body, mimetype='application/javascript')
        return response

    def _serve_report_main_js(self):
        dev = self._dev_tools.serve_dev_bundles
        body = f"var oap_config = {json.dumps(self._config(), cls=plotly.utils.PlotlyJSONEncoder)};\n"

        oap_app_id = os.getenv('OAP_APP_ID')
        body += f"var OAP_APP_ID = '{oap_app_id}';\n"
        body += f"var OAP_IN_STORE_ID = '{self.in_store_id}';\n"
        base_path = self.config.requests_pathname_prefix.rstrip('/')
        body += f"var OAP_BASE_PATH = '{base_path}';\n"

        # external js files
        external_links = self.config.external_scripts

        # system js files
        mode = "dev" if self._dev_tools["props_check"] is True else "prod"

        deps = []
        for js_dist_dependency in dash_renderer._js_dist_dependencies:
            dep = {}
            for key, value in js_dist_dependency.items():
                dep[key] = value[mode] if isinstance(value, dict) else value

            deps.append(dep)

        resources = (
            self.scripts._resources._filter_resources(deps, dev_bundles=dev)
          + self.scripts.get_all_scripts(dev_bundles=dev)
          + self.scripts._resources._filter_resources(dash_renderer._js_dist, dev_bundles=dev)
        )

        for resource in resources:
            is_dynamic_resource = resource.get("dynamic", False)

            if "relative_package_path" in resource:
                paths = resource["relative_package_path"]
                paths = [paths] if isinstance(paths, str) else paths

                for rel_path in paths:
                    self.registered_paths[resource["namespace"]].add(rel_path)

                    if not is_dynamic_resource:
                        _body = pkgutil.get_data(resource["namespace"], rel_path).decode("utf-8")
                        body += self.pre_process(_body, rel_path, dev)

        body += "var renderer = new DashRenderer();\n"

        response = flask.Response(body, mimetype='application/javascript')

        return response

    def pre_process(self, txt_body, file_name, dev):
        if file_name.startswith('dash_renderer.'):
            txt_body = txt_body.replace("JSON.parse(document.getElementById('_dash-config').textContent);", "oap_config;")  # in dev
            txt_body = txt_body.replace("JSON.parse(document.getElementById(\"_dash-config\").textContent);", "oap_config;")  # in live
            txt_body = txt_body.replace('react-entry-point', _report_content_entry_id_)
        
        return txt_body + "\n"

    def get_component_ids(self, layout):
        component_ids = []
        for component in layout._traverse():
            component_id = stringify_id(getattr(component, "id", None))
            component_ids.append(component_id)

        return component_ids

    def _layout_value(self):
        """
        add custom stores
        """
        _layout = self._layout() if self._layout_is_function else self._layout                        

        component_ids = self.get_component_ids(_layout)
        
        if self.in_store_id not in component_ids:
            _layout.children.append(dcc.Store(id="dummy-store"))
            _layout.children.append(dcc.Store(id=self.out_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id=self.in_store_id, storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-start-date', storage_type="local"))
            _layout.children.append(dcc.Store(id='op-filter-end-date'))

        return _layout

    def _generate_renderer(self):
        return ''

    def _generate_config_html(self):
        return ''

    def _generate_css_dist_html(self):
        return f'<link rel="stylesheet" href="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.css">'

    def _generate_scripts_html(self):
        return f'<script src="{self.config.requests_pathname_prefix}opsramp-analytics-utils/main.js"></script>'
