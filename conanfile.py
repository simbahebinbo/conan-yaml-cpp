import os
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy
from conan.tools.scm import Git


class PackageConan(ConanFile):
    name = "yaml-cpp"
    version = "0.6.2-0f9a586-p1"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/simbahebinbo/conan-yaml-cpp.git"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        git = Git(self)
        if not os.path.exists(os.path.join(self.source_folder, ".git")):
            git.clone("https://github.com/simbahebinbo/yaml-cpp.git", target=".")
        else:
            self.run("git pull")

        branch_name = "develop"
        git.checkout(branch_name)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # 头文件路径
        include_folder = os.path.join(self.source_folder, "include")
        # 库文件路径
        lib_folder = os.path.join(self.build_folder)

        copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=include_folder, keep_path=True)
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src=include_folder, keep_path=True)
        copy(self, "*.a", dst=os.path.join(self.package_folder, "lib"), src=lib_folder, keep_path=True)

    def package_info(self):
        self.cpp_info.libs = ["yaml-cpp"]
        self.cpp_info.includedirs = ["include"]
