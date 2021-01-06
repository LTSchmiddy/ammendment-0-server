from datetime import datetime

from typing import TypeVar, Generic, Union

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm import session
from sqlalchemy.orm.scoping import scoped_session

import core_db

from . import common

# Python will let us dynamically create class definitions at runtime.
# Wacky, but it definitely saves us some repetition.
def construct_var_table(p_type: type):
    class VarBase:       
        __tablename__ = 'vt_' + p_type.__name__
        
        v_type = p_type
        
        key = Column(Text, primary_key=True)
        value = Column(core_db.db_type_conversions[p_type], nullable=True)
        
        created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
        updated = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

        def __repr__(self):
            return f'<Var (type: {self.v_type}) {self.key}={self.value}>'

        @classmethod
        def get(cls, key: str, default: Union[p_type, None]=None) -> Union[p_type, None]:
            session = core_db.get_session()
            retVal = cls.get_s(session, key, default)
            session.remove()
            return retVal

        @classmethod
        def get_s(cls, session: scoped_session, key: str, default: Union[p_type, None]=None) -> Union[p_type, None]:
            return session.query(cls).filter(cls.key==key).first()
            # r_all = session.query(cls).filter(cls.key==key).all()
            # if len(r_all) <= 0:
                # return None
            
            # return r_all[0]
        
        
        # Return is based of whether a new entry was created for the varialble.
        @classmethod
        def set(cls, key: str, value: Union[p_type, None]=None) -> bool:
            session = core_db.get_session()
            retVal = cls.set_s(session, key, value)
            session.commit()
            session.remove()
            return retVal

        @classmethod
        def set_s(cls, session: scoped_session, key: str, value: Union[p_type, None]=None) -> bool:
            entry = session.query(cls).filter(cls.key==key).first()
            
            retVal = entry is None
            
            if retVal:
                entry = cls()
                entry.key = key
                
            entry.value = value
            entry.updated = datetime.utcnow()
            
            return retVal
    
    VarBase.__name__ = "Var" + p_type.__name__.capitalize()
    VarBase.__classname__ = "Var" + p_type.__name__.capitalize()
    
    return VarBase
        

class VarBool (core_db.Base, construct_var_table(bool)): pass
class VarInt (core_db.Base, construct_var_table(int)): pass
class VarFloat (core_db.Base, construct_var_table(float)): pass
class VarStr (core_db.Base, construct_var_table(str)): pass
class VarList (core_db.Base, construct_var_table(list)): pass
class VarDict (core_db.Base, construct_var_table(dict)): pass


__all__ = (
    'VarBool', 
    'VarInt', 
    'VarFloat', 
    'VarStr', 
    'VarList', 
    'VarDict', 
)