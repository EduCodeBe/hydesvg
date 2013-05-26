# -*- coding: utf-8 -*-
"""
Contains classes to handle images related things

# Requires PIL or pillow
"""

from hyde.plugin import CLTransformer

import os

from fswrap import File

class SVGPlugin(CLTransformer):
    """
    The plugin class for SVG
    """

    def __init__(self, site):
        super(SVGPlugin, self).__init__(site)

    @property
    def plugin_name(self):
        """
        The name of the plugin.
        """
        return "svg"

    def option_prefix(self, option):
        return "-"

    def text_resource_complete(self, resource, text):
        """
        If the site is in development mode, just return.
        Otherwise, run optipng to compress the png file.
        """

        if not resource.source_file.kind == 'svg':
            return

        source = File.make_temp(text)
        (source_root, source_ext) = os.path.splitext(unicode(source))

        png_in_source = source_root + u'.png'
        if os.path.exists(png_in_source):
            return text

        target = self.site.config.deploy_root_path.child(
                                resource.relative_deploy_path)
        (root, ext) = os.path.splitext(target)
        target = root + u'.png'

        d = os.path.dirname(target)
        if not os.path.exists(d):
            os.makedirs(d)
        args = [u'inkscape']
        args.extend(['-z'])
        args.extend(['-f', unicode(source)])
        args.extend(['-w', '850'])
        args.extend(['-h', '170'])
        args.extend(['-e', unicode(target)])
        print args
        self.call_app(args)
        return text
