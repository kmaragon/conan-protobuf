from conans import ConanFile, CMake, tools
import os
import re

class ProtobufConan(ConanFile):
    name = "Protobuf"
    version = "2.6.1"
    license = "https://raw.githubusercontent.com/google/protobuf/master/LICENSE"
    url = "https://github.com/google/protobuf"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_shared": [True, False],
        "build_static": [True, False],
        "use_static": [True, False]
    }

    default_options = "build_shared=True","build_static=True","use_static=False"
    generators = "cmake"
    description = "*nix only (for now) implementation of protobuf that can be used as a dep for other libs"

    def source(self):
        tools.download("https://github.com/google/protobuf/"
                       "releases/download/v2.6.1/protobuf-2.6.1.zip",
                       "protobuf.zip")

        tools.unzip("protobuf.zip")
        os.unlink("protobuf.zip")

        # autogen
        self.run("chmod +x protobuf-%s/autogen.sh" % self.version)
        self.run("cd protobuf-%s && ./autogen.sh" % self.version)

    def build(self):
        current_dir = os.getcwd()
        finished_package = current_dir + "/pkg"
        flags = "--enable-shared" if self.options.build_shared else "--disable-shared" + \
                "--enable-static" if self.options.build_static else "--disable-static"

        make_options = os.getenv("MAKEOPTS") or ""
        if not re.match("/[^A-z-a-z_-]-j", make_options):
            cpucount = tools.cpu_count()
            make_options += " -j %s" % (cpucount * 2)


        # configure
        self.run("chmod +x protobuf-%s/configure" % self.version)
        self.run("mkdir -p protobuf-%s/build" % self.version)
        self.run("cd protobuf-%s/build && ../configure --prefix=%s %s" % (self.version, finished_package, flags))

        # build
        self.run("cd protobuf-%s/build && make %s install" % (self.version, make_options))

    def package(self):
        self.copy("*", dst="lib", src="pkg/lib")
        self.copy("*", dst="bin", src="pkg/bin")
        self.copy("*", dst="include", src="pkg/include")

    def package_info(self):
        if self.settings.os == "Macos":
            self.cpp_info.libs = ["libprotobuf.a"] if self.options.use_static else ["libprotobuf.9.dylib"]
        else:
            self.cpp_info.libs = ["protobuf"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
