import pkgconfig


def gen_linker_flags(build_config):
    flags = gen_pkg_config_lib_flags(build_config["libraries"])
    flags += build_config['flags']['linker']
    flags.sort()
    return flags


def gen_compiler_flags(build_config):
    flags = gen_pkg_config_cc_flags(build_config["libraries"])
    flags += build_config['flags']['compiler']
    flags.sort()
    return flags


def gen_pkg_config_lib_flags(libraries):
    libFlags = []
    if len(libraries) > 0:
        for lib in libraries:
            try:
                libFlags += pkgconfig.libs(lib).split(" ")
            except Exception:
                pass
        return libFlags
    else:
        return []


def gen_pkg_config_cc_flags(libraries):
    cflags = []
    if len(libraries) > 0:
        for lib in libraries:
            try:
                cflags += pkgconfig.cflags(lib).split(" ")
            except Exception:
                pass
        return cflags
    else:
        return []
