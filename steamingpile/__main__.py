import docopt  # type: ignore

import steamingpile.config as appcfg
import steamingpile.appmain as appmain
import steamingpile.doc as appdoc

STEAMINGPILE_VERSION = 0.9

if __name__ == "__main__":
    opt = docopt.docopt(appdoc.__doc__, version=STEAMINGPILE_VERSION, options_first=True)

    conf = appcfg.SteamingPileConfig(opt)
    if conf.api_key() == "":
        raise RuntimeError("No personal API key found. Please see help (--help) for information.")

    sp = appmain.SteamingPile(conf)
    sp.run()
