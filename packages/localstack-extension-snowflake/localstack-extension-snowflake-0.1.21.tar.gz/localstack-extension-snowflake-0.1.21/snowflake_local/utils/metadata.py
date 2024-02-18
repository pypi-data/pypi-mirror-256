import dataclasses
from dataclasses import dataclass
from snowflake_local.engine.models import TableColumn
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.transform_utils import get_canonical_name
@dataclass
class TableSchema:table_name:str;columns:list[TableColumn]=dataclasses.field(default_factory=list)
class MetadataUtils:
	@classmethod
	def get_table_schema(G,table_name,database):
		A=table_name;A=get_canonical_name(A,quoted=False).strip('"');C=TableSchema(table_name=A);E=f"SELECT * FROM information_schema.columns WHERE table_name='{A}'";B=State.server.run_query(E,database=database);B=list(B)
		for D in B:F=TableColumn(name=D[3],type_name=D[7]);C.columns.append(F)
		return C