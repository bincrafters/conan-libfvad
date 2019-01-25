#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration


class LibfvadConan(ConanFile):
    name = "libfvad"
    version = "1.0"
    description = "Voice activity detection (VAD) library"
    topics = ("conan", "libvad", "voice", "vad")
    url = "https://github.com/bincrafters/conan-libfvad"
    homepage = "https://github.com/dpirch/libfvad"
    author = "TMiguelT <ttmigueltt@gmail.com>"
    license = "BSD-3-Clause"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True , False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _autotools = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.shared

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "gcc" and \
           Version(self.settings.compiler.version.value) < "5":
            raise ConanInvalidConfiguration("libfvad requires gcc > 4.9")
        elif self.settings.compiler == "Visual Studio":
            raise ConanInvalidConfiguration("libfvad is not supported for Visual Studio")

    def source(self):
        archive_url = "{0}/releases/download/v{1}/libfvad-{1}.tar.xz".format(self.homepage, self.version)
        tools.get(archive_url, sha256="09dd6f01ff91458bbcf411bc803b2f7d5825abda626f8adc6eea30c088a3859a")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            if self.settings.os == "Windows":
                args = [ "--enable-static=yes", "--enable-shared=no" ]
            else:
                args = [
                    "--enable-static=%s" % ("no" if self.options.shared else "yes"),
                    "--enable-shared=%s" % ("yes" if self.options.shared else "no")
                ]
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
