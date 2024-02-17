__version_tuple__=(0,0,5)
try:
  import MainHash.blake2b as blake2b
except Exception as error:
  print(error)
try:
  import MainHash.blake2s as blake2s
except Exception as error:
  print(error)
try:
  import MainHash.md5 as md5
except Exception as error:
  print(error)
try:
  import MainHash.sha1 as sha1
except Exception as error:
  print(error)
try:
  import MainHash.sha224 as sha224
except Exception as error:
  print(error)
try:
  import MainHash.sha256 as sha256
except Exception as error:
  print(error)
try:
  import MainHash.sha384 as sha384
except Exception as error:
  print(error)
try:
  import MainHash.sha3_224 as sha3_224
except Exception as error:
  print(error)
try:
  import MainHash.sha3_256 as sha3_256
except Exception as error:
  print(error)
try:
  import MainHash.sha3_384 as sha3_384
except Exception as error:
  print(error)
try:
  import MainHash.sha3_512 as sha3_512
except Exception as error:
  print(error)
try:
  import MainHash.sha512 as sha512
except Exception as error:
  print(error)
# try:
  # import MainHash.shake_128 as shake_128
# except Exception as error:
  # print(error)
# try:
  # import MainHash.shake_256 as shake_256
# except Exception as error:
  # print(error)
# Данные о модуле
__version__="{}.{}.{}".format(*__version_tuple__)
__depends__={
  "required":[
    "hashlib",
    "mainshortcuts"
    ],
  "optional":[]
  }
__functions__=[]
__classes__={}
__variables__=[]
__all__=__functions__+__variables__+list(__classes__.keys())
__scripts__=[
  "MainHash-check",
  "MainHash-gen",
  "MH-gen",
  "MH-check",
  ]
_algs=[
  "blake2b",
  "blake2s",
  "md5",
  "sha1",
  "sha224",
  "sha256",
  "sha384",
  "sha3_224",
  "sha3_256",
  "sha3_384",
  "sha3_512",
  "sha512",
  # "shake_128",
  # "shake_256",
  ]
_alg_functions=[
  "path",
  "file",
  "text",
  "bytes",
  ]
for i1 in _algs:
  for i2 in _alg_functions:
    __functions__.append(f"{i1}.{i2}")
__all__.sort()
__functions__.sort()
__scripts__.sort()
__variables__.sort()
_algs.sort()
