from conans import ConanFile, tools
import os
import re

class ProtobufConan(ConanFile):
    name = "Protobuf"
    version = "3.5.0"
    license = "https://raw.githubusercontent.com/google/protobuf/master/LICENSE"
    url = "https://github.com/kmaragon/conan-protobuf"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "with_zlib": [True, False]
    }

    default_options = "shared=True","with_zlib=True"
    generators = "virtualbuildenv"
    description = "*nix only (for now) implementation of protobuf that can be used as a dep for other libs"

    def configure(self):
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def source(self):
        tools.download("https://github.com/google/protobuf/archive/v%s.tar.gz" % self.version,
                       "protobuf.tar.gz")

        tools.unzip("protobuf.tar.gz")
        os.unlink("protobuf.tar.gz")

        # autogen
        self.run("chmod +x protobuf-%s/autogen.sh" % self.version)
        self.run("cd protobuf-%s && ./autogen.sh" % self.version)

    def build(self):
        flags = "--enable-shared" if self.options.shared else "--disable-shared" + \
                "--disable-static" if self.options.shared else "--enable-static"

        make_options = os.getenv("MAKEOPTS") or ""
        if not re.match("/[^A-z-a-z_-]-j", make_options):
            cpucount = tools.cpu_count()
            make_options += " -j %s" % cpucount 


        # configure
        self.run("chmod +x protobuf-%s/configure" % self.version)
        self.run("/bin/sh -c '. activate_build.* && cd protobuf-%s && ./configure --prefix=%s %s'" % (self.version, self.package_folder, flags))

        # build
        self.run("/bin/sh -c '. activate_build.* && cd protobuf-%s && make %s'" % (self.version, make_options))

    def package(self):
        self.run("cd protobuf-%s && make install" % self.version)

    def package_info(self):
        self.cpp_info.libs = ["protobuf"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
