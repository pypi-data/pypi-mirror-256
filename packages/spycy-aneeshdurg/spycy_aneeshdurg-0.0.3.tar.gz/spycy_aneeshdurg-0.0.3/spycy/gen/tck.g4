tck_List
           :  '[' SP? ( tck_ExpectedValue SP? ( ',' SP? tck_ExpectedValue SP? )* )? ']' ;

tck_Map
          :  '{' SP? ( oC_PropertyKeyName SP? ':' SP? tck_ExpectedValue SP? ( ',' SP? oC_PropertyKeyName SP? ':' SP? tck_ExpectedValue SP? )* )? '}' ;

tck_Literal
          : '-' SP? oC_NumberLiteral
              | oC_Literal
              ;

tck_Path
          : '<' SP? oC_AnonymousPatternPart SP? '>';

tck_ExpectedValue
          : ( tck_Map | tck_List | tck_Literal | tck_Path | oC_Pattern | oC_RelationshipDetail ) ;
