from conans import ConanFile, CMake, tools


class OpenBLASConan(ConanFile):
    name = "OpenBLAS"
    version = "0.2.20"
    license = "https://github.com/xianyi/OpenBLAS/blob/develop/LICENSE"
    url = "https://github.com/cinderblocks/conan-openblas"
    description = "OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/xianyi/OpenBLAS.git")
        self.run("cd OpenBLAS && git checkout tags/v0.2.20")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("OpenBLAS/CMakeLists.txt", "project(OpenBLAS)", '''project(OpenBLAS)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build_requirements(self):
        # useful for example for conditional build_requires
        if self.settings.os == "Windows":
            self.build_requires("nasm/2.13.01@conan/stable")

    def build(self):
        cmake = CMake(self)
        self.run('cmake OpenBLAS %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="OpenBLAS")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["OpenBLAS"]
