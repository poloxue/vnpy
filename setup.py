import sys
import platform
import subprocess
from pathlib import Path
from setuptools import setup, Extension


# Generate i18n mo files
python_path: Path = Path(sys.executable)
msgfmt_path: Path = python_path.parent.joinpath("Tools", "i18n", "msgfmt.py")

generate_mo_cmd = [
    str(python_path),
    str(msgfmt_path),
    "-o",
    ".\\vnpy\\trader\\locale\\en\\LC_MESSAGES\\vnpy.mo",
    ".\\vnpy\\trader\\locale\\en\\LC_MESSAGES\\vnpy",
]

subprocess.run(generate_mo_cmd)


def ctp_modules():
    libraries = ["thostmduserapi_se", "thosttraderapi_se"]

    # Linux
    if platform.system() == "Linux":
        include_dirs = ["vnpy/ctp/api/include", "vnpy/ctp/api/vnctp"]
        library_dirs = ["vnpy/ctp/api"]
        extra_compile_flags = [
            "-std=c++17",
            "-O3",
            "-Wno-delete-incomplete",
            "-Wno-sign-compare",
        ]
        extra_link_args = ["-lstdc++"]
        runtime_library_dirs = ["$ORIGIN"]
    elif platform.system() == "Window":
        include_dirs = ["vnpy/ctp/api/inlclude", "vnpy/ctp/api/vnpyctp"]
        library_dirs = ["vnpy/ctp/api/libs", "vnpy/ctp/api"]
        extra_compile_flags = ["-O2", "-MT"]
        extra_link_args = []
        runtime_library_dirs = []
    elif platform.system() == "Darwin":
        include_dirs = ["vnpy/ctp/api/include/mac", "vnpy/ctp/api/vnctp"]
        library_dirs = ["vnpy/ctp/api/libs"]
        extra_compile_flags = [
            "-std=c++11",
            "-mmacosx-version-min=10.12",
        ]
        extra_link_args = [
            "-mmacosx-version-min=10.12",
        ]

        framework_path = Path(__file__).parent.joinpath("vnpy/ctp", "api", "libs")
        runtime_library_dirs = [str(framework_path)]
    else:
        return []

    vnctpmd = Extension(
        name="vnpy.ctp.api.vnctpmd",
        sources=["vnpy/ctp/api/vnctp/vnctpmd/vnctpmd.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        language="cpp",
    )

    vnctptd = Extension(
        name="vnpy.ctp.api.vnctptd",
        sources=["vnpy/ctp/api/vnctp/vnctptd/vnctptd.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        language="cpp",
    )

    return [vnctptd, vnctpmd]


def ctptest_modules():
    if platform.system() == "Linux":
        extra_compile_flags = [
            "-std=c++17",
            "-O3",
            "-Wno-delete-incomplete",
            "-Wno-sign-compare",
        ]
        extra_link_args = ["-lstdc++"]
        runtime_library_dirs = ["$ORIGIN"]

    elif platform.system() == "Windows":
        extra_compile_flags = ["-O2", "-MT"]
        extra_link_args = []
        runtime_library_dirs = []

    else:
        return []

    vnctpmd = Extension(
        "vnpy.ctptest.api.vnctpmd",
        [
            "vnpy/ctptest/api/vnctp/vnctpmd/vnctpmd.cpp",
        ],
        include_dirs=["vnpy/ctptest/api/include", "vnpy/ctptest/api/vnctp"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy/ctptest/api/libs", "vnpy/ctptest/api"],
        libraries=["thostmduserapi_se", "thosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    vnctptd = Extension(
        "vnpy.ctptest.api.vnctptd",
        [
            "vnpy/ctptest/api/vnctp/vnctptd/vnctptd.cpp",
        ],
        include_dirs=["vnpy/ctptest/api/include", "vnpy/ctptest/api/vnctp"],
        define_macros=[],
        undef_macros=[],
        library_dirs=["vnpy/ctptest/api/libs", "vnpy/ctptest/api"],
        libraries=["thostmduserapi_se", "thosttraderapi_se"],
        extra_compile_args=extra_compile_flags,
        extra_link_args=extra_link_args,
        runtime_library_dirs=runtime_library_dirs,
        depends=[],
        language="cpp",
    )

    return [vnctptd, vnctpmd]


# Run setup
setup(ext_modules=ctp_modules() + ctptest_modules())
