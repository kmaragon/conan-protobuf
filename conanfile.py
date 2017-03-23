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
    default_options = "shared=True,static=True"
    generators = "cmake"

    def source(self):
        tools.download("https://github.com/google/protobuf/"
                       "releases/download/v2.6.1/protobuf-2.6.1.zip",
                       "protobuf.zip")

        tools.unzip("protobuf.zip")
        os.unlink("protobuf.zip")

    def build(self):
        current_dir = os.path.getcwd()
        finished_package = current_dir + "/pkg"
        flags = "--enable-shared" if self.options.build_shared else "--disable-shared" + \
                "--enable-static" if self.options.build_static else "--disable-static"

        make_options = os.getenv("MAKEOPTS")
        if not re.match("/[^A-z-a-z_-]-j"):
            cpucount = tools.cpu_count()
            make_options += " -j %s" % (cpucount * 2)

        self.run("mkdir -p build")
        self.run("cd build && ../configure --prefix=" + finished_package)
        self.run("cd build && make %s install" % make_options)

    def package(self):
        self.copy("lib", dst=".", src="pkg/lib")
        self.copy("bin", dst=".", src="pkg/bin")
        self.copy("include", dst=".", src="pkg/include")

    def package_info(self):
        if self.settings.os == "Macos":
            self.cpp_info.libs = ["libprotobuf.a"] if self.options.use_static else ["libprotobuf.9.dylib"]
        else:
            self.cpp_info.libs = ["protobuf"]
