"""
This module contain tests for src/data/make_dataset.py
"""

from src.data.make_dataset import SGF2DS
import pytest

@pytest.fixture
def sgf_files():
    """
    Fixtures that contain examples of games in sgf-format 
    and label of winner 
    """
    sgf_texts = [
        """
        PW[amybot-beginner]
        BR[31k]
        WR[21k]
        TM[86400]OT[14400 fischer]
        RE[B+16]
        SZ[9]
        """,
        """
        WR[10级]  KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[W+R]TM[1800]
        TC[1]TT[30]AP[foxwq]  ;B[pd];W[dp];B[cd];W[qp];B[fc];W[kq];
        B[cn];W[co];B[ck];W[dn];B[cm];W[dm];B[dl];W[fq];B[
        """,
        "RE[W+9.5]", 
        """
        PB[兆礼]  PW[CSGWQ]  BR[11级]  WR[10级]  
        KM[0]HA[1]RU[Japanese]AP[GNU Go:3.8]
        RE[W+69.0]TM[600]TC[1]
        """,
        """
        (;GM[1]FF[4]  SZ[19]  GN[]  DT[2017-02-03]  PB[äººå?¯è¡£ç¾è£å·³ç?«]  PW[æ?ã?å¾
]  BR[16çº§]  WR[18çº§]  KM[650]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[draw]TM[1252]TC[3]TT[30]  ;B[pp];W[pd];B[dd];W[dp];B[mq];W[nm];B[gc
        """,
        """
        RE[B+3.5] 
        RE[W+2]
        RE[W+R]
        """, 
        """BLABLABLAR[B+R]E]RE[drasw]"""
    ]
    winners = ["B", "W", "W", "W", "Draw", -1, -1]
    return zip(sgf_texts, winners)

def test_find_one_winner(sgf_files):
    """Test case when we have correct sgf-format (one winner in file)"""
    for sgf_text, winner in sgf_files:
        assert SGF2DS._find_winner(sgf_text) == winner
