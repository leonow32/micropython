# 2025.12.21

import binascii

text = 'The standard Lorem Ipsum passage, used since the 1500s"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"1914 translation by H. Rackham"But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?"Section 1.10.33 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC"At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."1914 translation by H. Rackham"On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."'

def sha256(data):
    """
    Edukacyjna implementacja SHA-256 – krok po kroku.
    """

    # ============================================================
    # KROK 1: Normalizacja danych wejściowych
    # ============================================================
    # Algorytm SHA-256 operuje na bajtach.
    # Jeśli dostajemy string, kodujemy go do UTF-8.

    if isinstance(data, str):
        message = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        message = bytes(data)
    else:
        raise TypeError("Argument musi być typu bytes, bytearray lub str")

    # ============================================================
    # KROK 2: Definicja stałych algorytmu
    # ============================================================
    # Są to stałe zdefiniowane w standardzie FIPS 180-4.
    # Używane są w każdej z 64 rund kompresji.

    round_constants = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    # Początkowe wartości hash (8 rejestrów po 32 bity)
    hash_values = [
        0x6a09e667,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ]

    # ============================================================
    # KROK 3: Funkcja pomocnicza – rotacja bitowa w prawo
    # ============================================================
    # SHA-256 intensywnie używa rotacji bitowych na 32-bitowych słowach.

    def rotate_right(value, bits):
        return ((value >> bits) | (value << (32 - bits))) & 0xffffffff

    # ============================================================
    # KROK 4: Padding (dopełnianie wiadomości)
    # ============================================================
    # 1. Zapamiętujemy długość wiadomości w bitach
    # 2. Dodajemy bit '1'
    # 3. Dodajemy zera aż długość ≡ 448 (mod 512)
    # 4. Dodajemy 64-bitową długość wiadomości

    message_length_bits = len(message) * 8

    # Dodanie bitu '1' → bajt 0x80
    message += b'\x80'

    # Dopełnianie zerami
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'

    # Dodanie długości wiadomości (64 bity, big endian)
    message += message_length_bits.to_bytes(8, 'big')

    # ============================================================
    # KROK 5: Przetwarzanie bloków 512-bitowych
    # ============================================================

    for block_start in range(0, len(message), 64):

        # Wyodrębnienie jednego bloku (64 bajty)
        block = message[block_start:block_start + 64]

        # ------------------------------------------------------------
        # KROK 5.1: Utworzenie harmonogramu wiadomości (message schedule)
        # ------------------------------------------------------------
        # W[0..15] pochodzi bezpośrednio z bloku
        # W[16..63] jest obliczane na podstawie wcześniejszych wartości

        message_schedule = [0] * 64

        for i in range(16):
            message_schedule[i] = int.from_bytes(
                block[i * 4:(i + 1) * 4],
                'big'
            )

        for i in range(16, 64):
            s0 = (
                rotate_right(message_schedule[i - 15], 7) ^
                rotate_right(message_schedule[i - 15], 18) ^
                (message_schedule[i - 15] >> 3)
            )
            s1 = (
                rotate_right(message_schedule[i - 2], 17) ^
                rotate_right(message_schedule[i - 2], 19) ^
                (message_schedule[i - 2] >> 10)
            )
            message_schedule[i] = (
                message_schedule[i - 16] +
                s0 +
                message_schedule[i - 7] +
                s1
            ) & 0xffffffff

        # ------------------------------------------------------------
        # KROK 5.2: Inicjalizacja rejestrów roboczych
        # ------------------------------------------------------------

        a, b, c, d, e, f, g, h = hash_values

        # ------------------------------------------------------------
        # KROK 5.3: 64 rundy funkcji kompresji
        # ------------------------------------------------------------

        for i in range(64):
            S1 = (
                rotate_right(e, 6) ^
                rotate_right(e, 11) ^
                rotate_right(e, 25)
            )
            ch = (e & f) ^ (~e & g)
            temp1 = (
                h +
                S1 +
                ch +
                round_constants[i] +
                message_schedule[i]
            ) & 0xffffffff

            S0 = (
                rotate_right(a, 2) ^
                rotate_right(a, 13) ^
                rotate_right(a, 22)
            )
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff

            # Przesunięcie rejestrów
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

        # ------------------------------------------------------------
        # KROK 5.4: Aktualizacja globalnego stanu hash
        # ------------------------------------------------------------

        hash_values = [
            (hash_values[0] + a) & 0xffffffff,
            (hash_values[1] + b) & 0xffffffff,
            (hash_values[2] + c) & 0xffffffff,
            (hash_values[3] + d) & 0xffffffff,
            (hash_values[4] + e) & 0xffffffff,
            (hash_values[5] + f) & 0xffffffff,
            (hash_values[6] + g) & 0xffffffff,
            (hash_values[7] + h) & 0xffffffff,
        ]

    # ============================================================
    # KROK 6: Złożenie wyniku końcowego
    # ============================================================
    # Każde z 8 słów 32-bitowych zamieniamy na 4 bajty.

    return b''.join(
        value.to_bytes(4, 'big') for value in hash_values
    )

print(binascii.hexlify(sha256(text)).decode().upper())