""""

"""


def extension_metadata():
    return {
        "primary_extension": True,
        "priority": 100,
        "setups": {
            "CTA": "dips://dcta-servers03.pic.es:9135/Configuration/Server,"
            "dips://dcta-agents03.pic.es:9135/Configuration/Server,"
            "dips://ctadirac-01.cscs.cta-observatory.org:9135/Configuration/Server,"
            "dips://ctadirac-02.cscs.cta-observatory.org:9135/Configuration/Server,"
            "dips://ctadirac-03.cscs.cta-observatory.org:9135/Configuration/Server,"
            "dips://ctadirac-04.cscs.cta-observatory.org:9135/Configuration/Server,"
            "dips://ctadirac-05.cscs.cta-observatory.org:9135/Configuration/Server,"
            "dips://cta-dirac.zeuthen.desy.de:9135/Configuration/Server",
            "CTA-cert": "dips://ccdcta-cert.in2p3.fr:9135/Configuration/Server",
        },
        "default_setup": "CTA",
    }
