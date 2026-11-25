def modInverse(n, m):
    """Código sacado de: https://www.geeksforgeeks.org/dsa/multiplicative-inverse-under-modulo-m/"""

    # Try all values from 1 to m-1
    for x in range(1, m):
        
        # Check if (n * x) % m == 1.
        # Note that n and x can be larger
        # than m, so we do modulo before
        # mulityplying
        if ((n % m) * (x % m)) % m == 1:
            return x

def cifrar_bytes_mensaje(bytes_mensaje: bytes | bytearray) -> bytes | bytearray:
    '''
    Recibe bytes y aplica en cada uno de ellos 
    el cifrado indicado en el enunciado:
        (b + 0x2A) % 256
    '''
    es_bytes = type(bytes_mensaje) is bytes
    retorno = bytearray()
    if isinstance(bytes_mensaje, bytes):
        bytes_mensaje = bytearray(bytes_mensaje)

    for i in range(len(bytes_mensaje)):
        retorno.append((bytes_mensaje[i] + int.from_bytes(b"0x2A")) % 256)

    if es_bytes:
        return bytes(retorno)
    return retorno

def descifrar_bytes_mensaje(bytes_mensaje: bytes | bytearray) -> bytes | bytearray:
    '''
    Recibe bytes cifrados y descifra cada uno de ellos
    '''
    es_bytes = type(bytes_mensaje) is bytes
    retorno = bytearray()
    if es_bytes:
        bytes_mensaje = bytearray(bytes_mensaje)

    for i in range(len(bytes_mensaje)):
        retorno.append((bytes_mensaje[i] - int.from_bytes(b"0x2A")) % 256)

    if es_bytes:
        return bytes(retorno)
    return retorno


if __name__ == '__main__':
    # Primer mensaje
    mensaje = 'Hola! Soy Pepa la tortuga 🐢🐢🐢'
    print('Mensaje original:  ', mensaje)

    bytes_mensaje = mensaje.encode('UTF-8')
    mensaje_cifrado = cifrar_bytes_mensaje(bytes_mensaje)
    print('Mensaje cifrado:   ', mensaje_cifrado)

    bytes_descifrados  = descifrar_bytes_mensaje(mensaje_cifrado)
    mensaje_descifrado = bytes_descifrados.decode('UTF-8')
    print('Mensaje descifrado:', mensaje_descifrado)

    print('¿Mismo mensaje?', mensaje == mensaje_descifrado)

    print('\n' + '-' * 20 + '\n')

    # Segundo mensaje
    mensaje = b'r\x99\x96\x8bKJ}\x99\xa3Jv\x9f\x98\x8bJ\x8f\x96J\x91' \
                      b'\x8b\x9e\x99JJJ\xa8Rg\x88\x0c\xaa\xcf\x88S\r\xad\xb8'
    print('Mensaje original:  ', mensaje)

    bytes_descifrados = descifrar_bytes_mensaje(mensaje)
    mensaje_descifrado = bytes_descifrados.decode('UTF-8')
    print('Mensaje descifrado:', mensaje_descifrado)

    bytes_mensaje = mensaje_descifrado.encode('UTF-8')
    mensaje_cifrado = cifrar_bytes_mensaje(bytes_mensaje)
    print('Mensaje cifrado:   ', mensaje_cifrado)

    print('¿Mismo mensaje?', mensaje == mensaje_cifrado)
