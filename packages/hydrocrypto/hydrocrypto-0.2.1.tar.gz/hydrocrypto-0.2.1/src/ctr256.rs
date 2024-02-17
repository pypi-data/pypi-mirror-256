use aes::{cipher::{generic_array::GenericArray, BlockEncrypt, KeyInit}, Aes256};

use crate::aes256::{AES_BLOCK_SIZE, AES_IV_SIZE};

pub fn ctr(data: &[u8], length: usize, key: &[u8], iv: &[u8], state: &[u8]) -> Vec<u8> {
    let cipher = Aes256::new(GenericArray::from_slice(key));
    let mut out = Vec::from(data);
    let mut state_array = [0u8; AES_IV_SIZE];
    state_array.copy_from_slice(state);
    let mut iv_array = [0u8; AES_IV_SIZE];
    iv_array.copy_from_slice(iv);
    let mut chunk = GenericArray::clone_from_slice(&iv);
    cipher.encrypt_block(&mut chunk);

    for i in (0..length).step_by(AES_BLOCK_SIZE) {
        for j in 0..std::cmp::min(length - i, 16) {
            out[i + j] ^= chunk[state_array[0] as usize];
            state_array[0] += 1;

            if (state_array[0] as usize) >= AES_BLOCK_SIZE {
                state_array[0] = 0;
            }

            if state_array[0] == 0 {
                for k in (0..AES_BLOCK_SIZE).rev() {
                    match iv_array[k].checked_add(1) {
                        Some(val) => {
                            iv_array[k] = val;
                            break;
                        }
                        None => {
                            iv_array[k] = 0
                        }
                    }
                }

                cipher.encrypt_block(&mut chunk);
            }
        }
    }

    out
}