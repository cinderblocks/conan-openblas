from conans import ConanFile, CMake, tools


class OpenBLASConan(ConanFile):
    name = "OpenBLAS"
    version = "0.2.20"
    license = "https://github.com/xianyi/OpenBLAS/blob/develop/LICENSE"
    url = "https://github.com/cinderblocks/conan-openblas"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "patch.diff"

    def source(self):
        self.run("git clone https://github.com/xianyi/OpenBLAS.git")
        self.run("cd OpenBLAS && git checkout tags/v0.2.20")
        # This patch contains a small hack that might be useful to guarantee
        # proper /MT /MD linkage in MSVC if the packaged project doesn't have
        # variables to set it properly
        # It also removed a dependence on awk because Window has poor quoting support
        self.run("cp patch.diff OpenBLAS && cd OpenBLAS && git apply patch.diff")

    def build(self):   
        cmake = CMake(self)
        self.run('cmake OpenBLAS %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="OpenBLAS")
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.dll", dst="bin", src="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["libopenblas", "kernel", "interface", "driver_level2", "driver_level3", "driver_others"]
