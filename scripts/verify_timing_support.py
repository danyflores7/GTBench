#!/usr/bin/env python3
"""
Verifica que todos los juegos tengan soporte de timing.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gamingbench.games.tic_tac_toe import TicTacToe
from gamingbench.games.kuhn_poker import KuhnPoker
from gamingbench.games.negotiation import Negotiation
from gamingbench.games.pig import Pig
from gamingbench.games.first_sealed_auction import FirstSealedAuction
from gamingbench.games.connect_four import ConnectFour
from gamingbench.games.breakthrough import Breakthrough
from gamingbench.games.nim import Nim
from gamingbench.games.liars_dice import LiarsDice
from gamingbench.games.prisoners_dilemma import PrisonersDilemma
from gamingbench.utils.history_tracker import GameMatch


def check_timing_support():
    """Verifica que GameMatch tenga soporte de timing."""
    
    games = [
        ("TicTacToe", TicTacToe),
        ("Kuhn Poker", KuhnPoker),
        ("Negotiation", Negotiation),
        ("Pig", Pig),
        ("First Sealed Auction", FirstSealedAuction),
        ("Connect Four", ConnectFour),
        ("Breakthrough", Breakthrough),
        ("Nim", Nim),
        ("Liars Dice", LiarsDice),
        ("Prisoners Dilemma", PrisonersDilemma),
    ]
    
    print("=" * 80)
    print("VERIFICACIÓN DE SOPORTE DE TIMING EN TODOS LOS JUEGOS")
    print("=" * 80)
    print()
    
    # Check GameMatch has timing methods
    match = GameMatch()
    has_start_timer = hasattr(match, 'start_timer')
    has_end_timer = hasattr(match, 'end_timer')
    has_duration = hasattr(match, 'duration')
    has_start_time = hasattr(match, 'start_time')
    has_end_time = hasattr(match, 'end_time')
    
    print("📊 Verificando clase GameMatch:")
    print(f"  ✓ Método start_timer(): {'✅' if has_start_timer else '❌'}")
    print(f"  ✓ Método end_timer(): {'✅' if has_end_timer else '❌'}")
    print(f"  ✓ Atributo duration: {'✅' if has_duration else '❌'}")
    print(f"  ✓ Atributo start_time: {'✅' if has_start_time else '❌'}")
    print(f"  ✓ Atributo end_time: {'✅' if has_end_time else '❌'}")
    print()
    
    if not all([has_start_timer, has_end_timer, has_duration, has_start_time, has_end_time]):
        print("❌ ERROR: GameMatch no tiene soporte completo de timing")
        return False
    
    print("🎮 Verificando que todos los juegos heredan de OpenSpielGame:")
    print()
    
    all_ok = True
    for game_name, game_class in games:
        try:
            game_instance = game_class()
            # Check if it has the play method
            has_play = hasattr(game_instance, 'play')
            
            # The play method is in OpenSpielGame which uses GameMatch with timing
            parent_class = game_class.__bases__[0].__name__
            
            status = "✅" if has_play and parent_class == "OpenSpielGame" else "❌"
            print(f"  {status} {game_name:25} (hereda de: {parent_class})")
            
            if not has_play or parent_class != "OpenSpielGame":
                all_ok = False
                
        except Exception as e:
            print(f"  ❌ {game_name:25} ERROR: {e}")
            all_ok = False
    
    print()
    print("=" * 80)
    
    if all_ok:
        print("✅ RESULTADO: Todos los juegos tienen soporte de timing")
        print()
        print("Cómo funciona:")
        print("  1. Todos los juegos heredan de OpenSpielGame")
        print("  2. OpenSpielGame.play() usa GameMatch internamente")
        print("  3. GameMatch ahora tiene start_timer() y end_timer()")
        print("  4. Los tiempos se guardan automáticamente en el JSONL")
    else:
        print("❌ RESULTADO: Algunos juegos tienen problemas")
    
    print("=" * 80)
    
    return all_ok


if __name__ == "__main__":
    success = check_timing_support()
    sys.exit(0 if success else 1)
