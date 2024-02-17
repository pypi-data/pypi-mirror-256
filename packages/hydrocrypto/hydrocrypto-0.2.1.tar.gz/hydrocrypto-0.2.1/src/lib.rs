use aes256::{AES_BLOCK_SIZE, AES_IV_SIZE, AES_KEY_SIZE};
use ctr256::ctr;
use ige256::{ige_encrypt, ige_decrypt};
use pyo3::{prelude::*, types::PyBytes};
mod aes256;
mod ige256;
mod ctr256;

#[pyfunction]
#[pyo3(text_signature = "(data, key, iv)")]
fn ige256_encrypt<'a>(py: Python<'a>, data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<&'a PyBytes> {
    if data.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data must not be empty"));
    }
    
    if data.len() % AES_BLOCK_SIZE != 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data size must match a multiple of 16 bytes"));
    }
    
    if key.len() != AES_KEY_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the key should be 32"));
    }

    if iv.len() != AES_IV_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the iv should be 32"));
    }

    let result = ige_encrypt(data, data.len(), key, iv);
    Ok(PyBytes::new(py, &result))
}

#[pyfunction]
#[pyo3(text_signature = "(data, key, iv)")]
fn ige256_decrypt<'a>(py: Python<'a>, data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<&'a PyBytes> {
    if data.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data must not be empty"));
    }
    
    if data.len() % AES_BLOCK_SIZE != 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data size must match a multiple of 16 bytes"));
    }
    
    if key.len() != AES_KEY_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the key should be 32"));
    }

    if iv.len() != AES_IV_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the iv should be 32"));
    }

    let result = ige_decrypt(data, data.len(), key, iv);
    Ok(PyBytes::new(py, &result))
}

#[pyfunction]
#[pyo3(text_signature = "(data, key, iv, state)")]
fn ctr256_encrypt<'a>(py: Python<'a>, data: &[u8], key: &[u8], iv: &[u8], state: &[u8]) -> PyResult<&'a PyBytes> {
    if data.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data must not be empty"));
    }
    
    if data.len() % AES_BLOCK_SIZE != 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data size must match a multiple of 16 bytes"));
    }
    
    if key.len() != AES_KEY_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the key should be 32"));
    }

    if iv.len() != AES_IV_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the iv should be 32"));
    }

    let result = ctr(data, data.len(), key, iv, state);
    Ok(PyBytes::new(py, &result))
}

#[pyfunction]
#[pyo3(text_signature = "(data, key, iv, state)")]
fn ctr256_decrypt<'a>(py: Python<'a>, data: &[u8], key: &[u8], iv: &[u8], state: &[u8]) -> PyResult<&'a PyBytes> {
    if data.len() == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data must not be empty"));
    }
    
    if data.len() % AES_BLOCK_SIZE != 0 {
        return Err(pyo3::exceptions::PyValueError::new_err("Data size must match a multiple of 16 bytes"));
    }
    
    if key.len() != AES_KEY_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the key should be 32"));
    }

    if iv.len() != AES_IV_SIZE {
        return Err(pyo3::exceptions::PyValueError::new_err("Size of the iv should be 32"));
    }

    let result = ctr(data, data.len(), key, iv, state);
    Ok(PyBytes::new(py, &result))
}


#[pymodule]
fn hydrocrypto(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ige256_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(ige256_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(ctr256_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(ctr256_decrypt, m)?)?;
    Ok(())
}
