from .base import HV
import jax.numpy as jnp
from jax import core
from jaxtyping import Array, ArrayLike
from typing import Sequence
import equinox as eqx
import quax
from einops import einsum, reduce
import numpy as np
import jax

__all__ = ["Fourier"]


def _fourier_add(x: ArrayLike, y: ArrayLike) -> ArrayLike:
    return x + y


def _fourier_mul(x: ArrayLike, y: ArrayLike) -> ArrayLike:
    return x * y


def _fourier_div(x: ArrayLike, y: ArrayLike) -> ArrayLike:
    return x / y


class Fourier(HV):
    """
    Implements the Real-valued Multiply-Add-Permute VSA type.
    Elements are real valued numbers

    This type is used commonly with Random Fourier Features
    """

    def __init__(self, shape: tuple[int, ...] | None = None, **kwargs):
        """
        Initializes the Fourier VSA with the provided shape or data
        If no data is given, a vector is sampled randomly from a normal distribution

        Args:
            shape: The shape of the Fourier
            data(optional): The data of the Fourier

        Either one of shape/data must be provided

        Raises:
            ValueError: If neither shape nor data is provided
        """
        if "array" in kwargs:
            _data = kwargs["array"]
        elif shape is None:
            raise ValueError("shape must be provided if data is not")
        else:
            _data = self._init(shape)

        super().__init__(_data)

    def _init(self, shape: tuple[int, ...]):
        vecs = np.random.normal(size=shape)

        return vecs

    @classmethod
    def empty(cls, shape) -> "Fourier":
        return cls(array=jnp.zeros(shape))

    @staticmethod
    def default(
        primitive: core.Primitive,
        values: Sequence[ArrayLike],
        params: dict,
    ):
        raw_values: list[ArrayLike] = []
        for value in values:
            if eqx.is_array_like(value):
                raw_values.append(value)
            elif isinstance(value, Fourier):
                raw_values.append(value.array)
            else:
                assert False  # should never happen
        # print(raw_values, primitive, **params)
        out = primitive.bind(*raw_values, **params)
        if primitive.multiple_results:
            return [Fourier(x) for x in out]
        else:
            return Fourier(array=out)

    @jax.jit
    def __add__(self, other: "Fourier" | ArrayLike) -> "Fourier":
        """
        Implements bundling between Fourier hypervectors.
        Bundling for fourier hypervectors is the element-wise addition of the vectors

        Args:
            other: The other hypervector to bundle with

        Returns:
            The bundled hypervector
        """
        return quax.quaxify(_fourier_add)(self, other)  # type: ignore

    @jax.jit
    def __sub__(self, other: "Fourier" | ArrayLike) -> "Fourier":
        """
        Implements bundling between Fourier hypervectors (negation)

        Args:
            other: The other hypervector to bundle with

        Returns:
            The bundled hypervector
        """
        return quax.quaxify(_fourier_add)(self, -other)  # type: ignore

    @jax.jit
    def __mul__(self, other: "Fourier" | ArrayLike) -> "Fourier":
        """
        Implements binding between Fourier hypervectors
        Binding for fourier hypervectors is the element-wise multiplication or haddamard product of the vectors

        Args:
            other: The other hypervector to bind with

        Returns:
            The bound hypervector
        """
        return quax.quaxify(_fourier_mul)(self, other)  # type: ignore

    @jax.jit
    def __truediv__(self, other: "Fourier" | ArrayLike) -> "Fourier":
        return quax.quaxify(_fourier_div)(self, other)  # type: ignore

    def __neg__(self) -> "Fourier":
        """
        Negates the hypervector
        """
        res = quax.quaxify(_fourier_mul)(self, -1)  # type: ignore
        return res

    def __invert__(self) -> "Fourier":
        """
        Computes the inverse of the hypervector.
        For fourier hypervectors, this is the element-wise inverse of the vector
        """
        res = 1 / self.array
        return Fourier(array=res)

    def __rshift__(self, shifts: int) -> "Fourier":
        """
        Implements circular right shift of the hypervector. This is equivalent to permuting the hypervector

        Args:
            shifts: The number of shifts to perform

        Returns:
            The permuted hypervector
        """
        return Fourier(array=jnp.roll(self.array, shifts, axis=-1))

    def __lshift__(self, shifts: int) -> "Fourier":
        """
        Implements circular left shift of the hypervector. This is equivalent to permuting the hypervector

        Args:
            shifts: The number of shifts to perform

        Returns:
            The permuted hypervector
        """
        return Fourier(array=jnp.roll(self.array, -shifts, axis=-1))

    def __getitem__(self, item: int | slice) -> "Fourier":
        return Fourier(array=self.array[item])

    @jax.jit
    def dot(self, other: "Fourier") -> Array:
        """
        Computes the dot similarity between two sets hypervectors

        Note: This function computes the similarity between pairs of hypervectors

        Args:
            other: The other hypervector to compute the dot similarity with

        Returns:
            Arraylike: The dot similarity between the hypervectors
        """
        _dot = einsum(self.array, other.array, "i j,i j->i")

        return _dot

    @jax.jit
    def dota(self, other: "Fourier") -> Array:
        """
        Computes the dot similarity between two sets hypervectors

        Note: This function computes the similarity between every pair of hypervectors in the two sets

        Args:
            other: The other hypervector to compute the dot similarity with

        Returns:
            Arraylike: The dot similarity between the hypervectors
        """

        _dotm = einsum(self.array, other.array, "m d, n d->m n")

        return _dotm

    @jax.jit
    def csim(self, other: "Fourier") -> Array:
        """
        Computes the cosine similarity between pairs of hypervectors

        Args:
            other: The other hypervector to compute the cosine similarity with

        Returns:
            Arraylike: The cosine similarity between the hypervectors
        """
        _a = self.array / jnp.linalg.norm(self.array, axis=-1, keepdims=True)
        _b = other.array / jnp.linalg.norm(other.array, axis=-1, keepdims=True)
        csim = einsum(_a, _b, "i j,i j->i")

        return csim

    @jax.jit
    def csima(self, other: "Fourier") -> Array:
        """
        Computes the cosine similarity between every pair of hypervectors in the two sets

        Args:
            other: The other hypervector to compute the cosine similarity with

        Returns:
            Arraylike: The cosine similarity between the hypervectors
        """
        _a = self.array / jnp.linalg.norm(self.array, axis=-1, keepdims=True)
        _b = other.array / jnp.linalg.norm(other.array, axis=-1, keepdims=True)
        csim = einsum(_a, _b, "m d,n d->m n")

        return csim

    @jax.jit
    def set(self) -> "Fourier":
        """
        Bundles together an array of hypervectors to form a single hypervector

        Returns:
            The bundled hypervector
        """
        _res = reduce(self.array, "i j-> 1 j", "sum")
        return Fourier(array=_res)

    @jax.jit
    def mbind(self) -> "Fourier":
        """
        Binds together an array of hypervectors to form a single hypervector

        Returns:
            The bound hypervector
        """
        _res = reduce(self.array, "i j-> 1 j", "prod")
        return Fourier(array=_res)
