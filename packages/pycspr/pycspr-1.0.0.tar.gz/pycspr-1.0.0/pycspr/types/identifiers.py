import dataclasses
import enum
import typing


# The output of a one way hashing function.
Digest = typing.Union[bytes, str]

# An account identifier may be a byte array of 33 bytes,
# a hexadecimal string of 66 characters.
AccountID = typing.Union[bytes, str]

# A block identifier may be a byte array of 32 bytes,
# a hexadecimal string of 64 characters or a positive integer.
BlockID = typing.Union[bytes, str, int]

# On chain contract identifier.
ContractID = typing.NewType("Static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A deploy identifier is a 32 byte array or it's hexadecimal string equivalent.
DeployID = typing.Union[bytes, str]

# A purse identifier under which an account balance resides.
PurseID = typing.Union[bytes, object]


PublicKey = typing.Union[bytes, str]
URef = str
PurseID = typing.Union[AccountID, PublicKey, URef]


class PurseIDType(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    PublicKey = enum.auto()
    AccountHash = enum.auto()
    URef = enum.auto()


class GlobalStateIDType(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    # TODO: extend -> BlockHash`, `BlockHeight`, `StateRootHash
    STATE_ROOT = enum.auto()
    BLOCK = enum.auto()


@dataclasses.dataclass
class GlobalStateID():
    # 32 byte global state identifier, either a block or state root hash.
    identifier: typing.Union[bytes, int]

    # Type of identifier.
    id_type: GlobalStateIDType


# Root hash of a node's global state.
StateRootHash = typing.NewType(
    "Cumulative hash of block execution effects over global state.",
    bytes
    )


@dataclasses.dataclass
class DictionaryID():
    """A set of variants for performation dictionary item state queries.

    """
    pass


@dataclasses.dataclass
class DictionaryID_AccountNamedKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via an Account's named keys.

    """
    # The account key as a formatted string whose named keys contains dictionary_name.
    account_key: str

    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.account_key == other.account_key and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name


@dataclasses.dataclass
class DictionaryID_ContractNamedKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via a Contract's named keys.

    """
    # The contract key as a formatted string whose named keys contains dictionary_name.
    contract_key: str

    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.contract_key == other.contract_key and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name


@dataclasses.dataclass
class DictionaryID_SeedURef(DictionaryID):
    """Encapsulates information required to query a dictionary item
       via it's seed unforgeable reference.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: object

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.seed_uref == other.seed_uref


@dataclasses.dataclass
class DictionaryID_UniqueKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via it's unique key.

    """
    # The globally unique dictionary key.
    key: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.key == other.key
