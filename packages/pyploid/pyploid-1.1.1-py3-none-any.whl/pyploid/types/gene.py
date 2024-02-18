from collections import defaultdict
from collections.abc import Iterable
from copy import deepcopy
from dataclasses import dataclass, field, replace
from typing import TypeVar, NewType, Protocol, runtime_checkable, cast

from pyploid.types.cytogenetic_index import IndexType, ComplexPolyploidIndexType, SecondaryIndexType

T = TypeVar('T')
ValueType = TypeVar('ValueType')


GeneID = NewType('GeneID', str)


@dataclass(frozen=True)
class GeneDescription:
    uuid: GeneID
    allele_type: type
    description: str | None = field(default=None)


class Gene(Protocol[IndexType]):
    position: IndexType


@runtime_checkable
@dataclass(frozen=True)
class DataclassGene(Gene[IndexType], Protocol[IndexType]):
    position: IndexType


GeneType = TypeVar('GeneType')


def transform_position(
        gene: Gene[IndexType] | DataclassGene[IndexType], position: SecondaryIndexType
) -> Gene[SecondaryIndexType]:
    if isinstance(gene, DataclassGene):
        return replace(cast(DataclassGene[SecondaryIndexType], gene), position=position)
    else:
        cast(Gene[SecondaryIndexType], gene).position = position
        return cast(Gene[SecondaryIndexType], gene)


def update_position(gene: Gene[IndexType] | DataclassGene[IndexType], position: IndexType) -> Gene[IndexType]:
    if isinstance(gene, DataclassGene):
        return replace(gene, position=position)
    else:
        gene.position = position
        return gene


def reindex_chromosome_sets(
        genes: Iterable[Gene[ComplexPolyploidIndexType]]
) -> Iterable[Gene[ComplexPolyploidIndexType]]:
    indices: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for gene in genes:
        position: ComplexPolyploidIndexType = gene.position
        new_set_index: int = indices[position.chromosome_number][position.index]
        yield update_position(gene, position.reindex(position.chromosome_number, new_set_index, position.index))
        indices[position.chromosome_number][position.index] += 1
