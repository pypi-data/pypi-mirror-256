use num_bigint::{BigInt, Sign};

use crate::{ClvmDecoder, FromClvmError};

pub trait FromClvm<N>: Sized {
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError>;
}

macro_rules! clvm_primitive {
    ($primitive:ty) => {
        impl<N> FromClvm<N> for $primitive {
            fn from_clvm(
                decoder: &impl ClvmDecoder<Node = N>,
                node: N,
            ) -> Result<Self, FromClvmError> {
                const LEN: usize = std::mem::size_of::<$primitive>();

                let bytes = decoder.decode_atom(&node)?;
                let number = BigInt::from_signed_bytes_be(bytes);
                let (sign, mut vec) = number.to_bytes_be();

                if vec.len() < std::mem::size_of::<$primitive>() {
                    let mut zeros = vec![0; LEN - vec.len()];
                    zeros.extend(vec);
                    vec = zeros;
                }

                let value = <$primitive>::from_be_bytes(vec.as_slice().try_into().or(Err(
                    FromClvmError::WrongAtomLength {
                        expected: LEN,
                        found: bytes.len(),
                    },
                ))?);

                Ok(if sign == Sign::Minus {
                    value.wrapping_neg()
                } else {
                    value
                })
            }
        }
    };
}

clvm_primitive!(u8);
clvm_primitive!(i8);
clvm_primitive!(u16);
clvm_primitive!(i16);
clvm_primitive!(u32);
clvm_primitive!(i32);
clvm_primitive!(u64);
clvm_primitive!(i64);
clvm_primitive!(u128);
clvm_primitive!(i128);
clvm_primitive!(usize);
clvm_primitive!(isize);

impl<N, A, B> FromClvm<N> for (A, B)
where
    A: FromClvm<N>,
    B: FromClvm<N>,
{
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        let (first, rest) = decoder.decode_pair(&node)?;
        let first = A::from_clvm(decoder, first)?;
        let rest = B::from_clvm(decoder, rest)?;
        Ok((first, rest))
    }
}

impl<N> FromClvm<N> for () {
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        let bytes = decoder.decode_atom(&node)?;
        if bytes.is_empty() {
            Ok(())
        } else {
            Err(FromClvmError::WrongAtomLength {
                expected: 0,
                found: bytes.len(),
            })
        }
    }
}

impl<N, T, const LEN: usize> FromClvm<N> for [T; LEN]
where
    T: FromClvm<N>,
{
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, mut node: N) -> Result<Self, FromClvmError> {
        let mut items = Vec::with_capacity(LEN);
        loop {
            if let Ok((first, rest)) = decoder.decode_pair(&node) {
                if items.len() >= LEN {
                    return Err(FromClvmError::ExpectedAtom);
                } else {
                    items.push(T::from_clvm(decoder, first)?);
                    node = rest;
                }
            } else {
                let bytes = decoder.decode_atom(&node)?;
                if bytes.is_empty() {
                    return items.try_into().or(Err(FromClvmError::ExpectedPair));
                } else {
                    return Err(FromClvmError::WrongAtomLength {
                        expected: 0,
                        found: bytes.len(),
                    });
                }
            }
        }
    }
}

impl<N, T> FromClvm<N> for Vec<T>
where
    T: FromClvm<N>,
{
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, mut node: N) -> Result<Self, FromClvmError> {
        let mut items = Vec::new();
        loop {
            if let Ok((first, rest)) = decoder.decode_pair(&node) {
                items.push(T::from_clvm(decoder, first)?);
                node = rest;
            } else {
                let bytes = decoder.decode_atom(&node)?;
                if bytes.is_empty() {
                    return Ok(items);
                } else {
                    return Err(FromClvmError::WrongAtomLength {
                        expected: 0,
                        found: bytes.len(),
                    });
                }
            }
        }
    }
}

impl<N, T> FromClvm<N> for Option<T>
where
    T: FromClvm<N>,
{
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        if let Ok(&[]) = decoder.decode_atom(&node) {
            Ok(None)
        } else {
            Ok(Some(T::from_clvm(decoder, node)?))
        }
    }
}

impl<N> FromClvm<N> for String {
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        let bytes = decoder.decode_atom(&node)?;
        Ok(Self::from_utf8(bytes.to_vec())?)
    }
}

#[cfg(feature = "chia-bls")]
impl<N> FromClvm<N> for chia_bls::PublicKey {
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        let bytes = decoder.decode_atom(&node)?;
        let error = Err(FromClvmError::WrongAtomLength {
            expected: 48,
            found: bytes.len(),
        });
        let bytes = bytes.try_into().or(error)?;
        Self::from_bytes(bytes).map_err(|error| FromClvmError::Custom(error.to_string()))
    }
}

#[cfg(feature = "chia-bls")]
impl<N> FromClvm<N> for chia_bls::Signature {
    fn from_clvm(decoder: &impl ClvmDecoder<Node = N>, node: N) -> Result<Self, FromClvmError> {
        let bytes = decoder.decode_atom(&node)?;
        let error = Err(FromClvmError::WrongAtomLength {
            expected: 96,
            found: bytes.len(),
        });
        let bytes = bytes.try_into().or(error)?;
        Self::from_bytes(bytes).map_err(|error| FromClvmError::Custom(error.to_string()))
    }
}

#[cfg(test)]
mod tests {
    use crate::tests::{str_to_node, TestAllocator, TestNode};

    use super::FromClvm;
    use super::*;

    fn decode<T>(hex: &str) -> Result<T, FromClvmError>
    where
        T: FromClvm<TestNode>,
    {
        let mut a = TestAllocator::new();
        let (rest, actual) = str_to_node(&mut a, hex);
        assert_eq!(rest, "");
        T::from_clvm(&a, actual)
    }

    #[test]
    fn test_primitives() {
        assert_eq!(decode("NIL"), Ok(0u8));
        assert_eq!(decode("NIL"), Ok(0i8));
        assert_eq!(decode("05"), Ok(5u8));
        assert_eq!(decode("05"), Ok(5u32));
        assert_eq!(decode("05"), Ok(5i32));
        assert_eq!(decode("e5"), Ok(-27i32));
        assert_eq!(decode("NIL"), Ok(-0));
        assert_eq!(decode("80"), Ok(-128i8));
    }

    #[test]
    fn test_pair() {
        assert_eq!(decode("( 05 02"), Ok((5, 2)));
        assert_eq!(decode("( b8 ( 016009 NIL"), Ok((-72, (90121, ()))));
        assert_eq!(
            decode("( ( NIL ( NIL ( NIL ( ( NIL ( NIL ( NIL NIL NIL NIL"),
            Ok((((), ((), ((), (((), ((), ((), ()))), ())))), ()))
        );
    }

    #[test]
    fn test_nil() {
        assert_eq!(decode("NIL"), Ok(()));
    }

    #[test]
    fn test_array() {
        assert_eq!(decode("( 01 ( 02 ( 03 ( 04 NIL"), Ok([1, 2, 3, 4]));
        assert_eq!(decode("NIL"), Ok([] as [i32; 0]));
    }

    #[test]
    fn test_vec() {
        assert_eq!(decode("( 01 ( 02 ( 03 ( 04 NIL"), Ok(vec![1, 2, 3, 4]));
        assert_eq!(decode("NIL"), Ok(Vec::<i32>::new()));
    }

    #[test]
    fn test_option() {
        assert_eq!(decode("68656c6c6f"), Ok(Some("hello".to_string())));
        assert_eq!(decode("NIL"), Ok(None::<String>));

        // Empty strings get decoded as None instead, since both values are represented by nil bytes.
        // This could be considered either intended behavior or not, depending on the way it's used.
        assert_ne!(decode("NIL"), Ok(Some("".to_string())));
    }

    #[test]
    fn test_string() {
        assert_eq!(decode("68656c6c6f"), Ok("hello".to_string()));
        assert_eq!(decode("NIL"), Ok("".to_string()));
    }

    #[cfg(feature = "chia-bls")]
    #[test]
    fn test_public_key() {
        use chia_bls::PublicKey;
        use hex_literal::hex;

        let valid_bytes = hex!("b8f7dd239557ff8c49d338f89ac1a258a863fa52cd0a502e3aaae4b6738ba39ac8d982215aa3fa16bc5f8cb7e44b954d");
        assert_eq!(
            decode(&hex::encode(valid_bytes)),
            Ok(PublicKey::from_bytes(&valid_bytes).unwrap())
        );
        assert_eq!(
            decode::<PublicKey>("68656c6c6f"),
            Err(FromClvmError::WrongAtomLength {
                expected: 48,
                found: 5
            })
        );
    }

    #[cfg(feature = "chia-bls")]
    #[test]
    fn test_signature() {
        use chia_bls::Signature;
        use hex_literal::hex;

        let valid_bytes = hex!("a3994dc9c0ef41a903d3335f0afe42ba16c88e7881706798492da4a1653cd10c69c841eeb56f44ae005e2bad27fb7ebb16ce8bbfbd708ea91dd4ff24f030497b50e694a8270eccd07dbc206b8ffe0c34a9ea81291785299fae8206a1e1bbc1d1");
        assert_eq!(
            decode(&hex::encode(valid_bytes)),
            Ok(Signature::from_bytes(&valid_bytes).unwrap())
        );
        assert_eq!(
            decode::<Signature>("68656c6c6f"),
            Err(FromClvmError::WrongAtomLength {
                expected: 96,
                found: 5
            })
        );
    }
}
