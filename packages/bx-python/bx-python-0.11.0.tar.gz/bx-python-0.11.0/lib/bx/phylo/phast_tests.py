"""
Tests for `bx.phylo.phast`.
"""

from io import StringIO

from numpy import (
    allclose,
    array,
)

from bx.phylo.phast import TreeModel

test_data = """ALPHABET: A C G T - 
ORDER: 0
SUBST_MOD: HKY85+Gap
TRAINING_LNL: -178667772.836697
BACKGROUND: 0.227006 0.169993 0.169307 0.227262 0.206432 
RATE_MAT:
  -0.971735    0.122443    0.465361    0.163692    0.220238 
   0.163508   -1.130351    0.121949    0.624656    0.220238 
   0.623952    0.122443   -1.130326    0.163692    0.220238 
   0.163508    0.467247    0.121949   -0.972942    0.220238 
   0.242187    0.181362    0.180630    0.242461   -0.846640 
TREE: ((((((hg16:0.007738,panTro1:0.008356):0.027141,(baboon:0.009853,rheMac1:0.010187):0.035049):0.103138,galago:0.174770):0.019102,((rn3:0.092633,mm6:0.089667):0.273942,rabbit:0.230839):0.021927):0.023762,(canFam1:0.204637,(elephant:0.123777,tenrec:0.278910):0.085977):0.009439):0.306466,monDom1:0.401151)mammals;
"""  # noqa: W291


def test_parser():
    tm = TreeModel.from_file(StringIO(test_data))
    assert tm.alphabet == ("A", "C", "G", "T", "-")
    assert tm.order == 0
    assert tm.subst_mod == "HKY85+Gap"
    assert allclose(tm.background, [0.227006, 0.169993, 0.169307, 0.227262, 0.206432])
    assert allclose(
        tm.matrix,
        array(
            [
                [-0.971735, 0.122443, 0.465361, 0.163692, 0.220238],
                [0.163508, -1.130351, 0.121949, 0.624656, 0.220238],
                [0.623952, 0.122443, -1.130326, 0.163692, 0.220238],
                [0.163508, 0.467247, 0.121949, -0.972942, 0.220238],
                [0.242187, 0.181362, 0.180630, 0.242461, -0.846640],
            ]
        ),
    )
    assert (
        tm.tree
        == "((((((hg16:0.007738,panTro1:0.008356):0.027141,(baboon:0.009853,rheMac1:0.010187):0.035049):0.103138,galago:0.174770):0.019102,((rn3:0.092633,mm6:0.089667):0.273942,rabbit:0.230839):0.021927):0.023762,(canFam1:0.204637,(elephant:0.123777,tenrec:0.278910):0.085977):0.009439):0.306466,monDom1:0.401151)mammals;"
    )
