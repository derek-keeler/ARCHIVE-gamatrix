import docopt  # type: ignore

import gamatrix.appmain as appmain
import gamatrix.config as appcfg
import gamatrix.doc as appdoc

GAMATRIX_VERSION = 0.9

if __name__ == "__main__":
    opt = docopt.docopt(appdoc.__doc__, version=GAMATRIX_VERSION, options_first=True)

    conf = appcfg.GamatrixConfig(opt)
    if conf.api_key() == "":
        raise RuntimeError(
            "No personal API key found. Please see help (--help) for information."
        )

    sp = appmain.Gamatrix(conf)
    sp.run()
