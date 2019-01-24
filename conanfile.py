#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class LibnameConan(ConanFile):
    name = "libfvad"
    version = "1.0"
    description = "Voice activity detection (VAD) library"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("voice", "vad")
    url = "https://github.com/TMiguelT/conan-libfvad"
    homepage = "https://github.com/dpirch/libfvad"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        source_url = "https://github.com/dpirch/libfvad"

        archive_url = "{0}/releases/download/v{1}/libfvad-{1}.tar.xz".format(source_url, self.version)
        tools.get(archive_url, sha256="09dd6f01ff91458bbcf411bc803b2f7d5825abda626f8adc6eea30c088a3859a")
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure()
            env_build.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

        include_folder = os.path.join(self._source_subfolder, "include")
        lib_folder = os.path.join(self._source_subfolder, "src", ".libs")

        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", src=lib_folder, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=lib_folder, keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=lib_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
