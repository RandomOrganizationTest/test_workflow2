from conans import ConanFile, CMake

class TestWorkflow2(ConanFile): 
    name = "test_workflow2"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "txt"
    exports_sources = "CMakeLists.txt", "src/*", "include/*"
    options = {
        "coverage": [False, True]
    }
    default_options = {
        "coverage" : False
    }

    def build_requirements(self):
        self.build_requires("cmake-common-options/[^1.0.0, loose=False]")

    def imports(self):
        self.copy("commonoptions.cmake")

    def requirements(self):
        self.requires("test_workflow/[^1.0.0, loose=False]")

    def build(self):
        cmake = CMake(self)
        if self.options.coverage:
            cmake.definitions["CONAN_C_FLAGS"] += " -fprofile-arcs -ftest-coverage"
            cmake.definitions["CONAN_CXX_FLAGS"] += " -fprofile-arcs -ftest-coverage"
        cmake.configure()
        cmake.build()
        cmake.test()
        if self.options.coverage:
            self.run('gcovr -r %s' % (self.source_folder))

    def package(self):
        self.copy("*.a", dst="lib", src="lib")
        self.copy("*.hpp", dst="include", src="include")

    def package_info(self):
        self.cpp_info.libs = ["test_workflow2-static"]