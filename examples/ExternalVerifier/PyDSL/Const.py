CONSTRAINTS_OVERWRITING_WARNING = "Overwriting constraint for '{0}'. Only use a single @constraint decorator."

CONSTRAINT_DEFAULT_FAILED_ERROR_MSG = "Invalid custom type '{0}'{1}"
CONSTRAINT_CUSTOM_FN_FAILED_MSG = "Custom constraint function for type '{0}' failed with error:\n{1}\nThis may happen because the type is instantiated with invalid types, which are only validated after the constraint is checked.\n\nFull trace:\n{2}"
CONSTRAINT_CUSTOM_FN_FAILED_SHORT_MSG = "Custom constraint function for type '{0}' threw exception."
CONSTRAINT_WRONG_BASIC_TYPES = "Invalid type arguments. Expected '{0}', got '{1}'."

ATTRIBUTE_CONSTRAINT_DEFAULT_FAILED_ERROR_MSG = "Invalid attribute of class '{0}' with type '{1}'"

NESTED_UNION_TOO_FEW_ARGUMENTS = "Nested union requires two or more arguments."

PLUGIN_VERSION_WARNING = "The custom PyDSLPlugin for MyPy was not tested with your MyPy version {0}."

PARSE_TYPE_UNEXPECTED_RAW = "Encountered unexpected raw type {0}"
PARSE_TYPE_UNKNOWN_RAW_TYPE_WARNING = "Could not determine raw type for {0}"

REWRITE_LITERALS_NOP = "rewrite_literals could not find any literals to rewrite."

TESTED_VERSIONS = ["0.950"]

VALIDATE_TYPE_MISSING_RAW = "Could not perform validation because the raw types are missing."
VALIDATE_PYTYPES_IS_OF_TYPE_ERROR = "is_of_type({0}, {1}) from pytypes failed with exception:\n{2}"

VISITOR_NOT_IMPLEMENTED = "Visit function for '{0}' not implemented yet."
VISITOR_INSTANCE_EXPECTED_LIST = "Return values of query_types expected to be lists, instead got '{0}', '{1}'"
VISITOR_INSTANCE_UNEXPECTED_ARGS_NR = "query_types call in instance visitor returned an unexpected number of results.\ntypes: '{0}', raw: '{1}'"

TYPE_TO_LITERAL_UNKNOWN_INSTANCE = "Unknown instance ignored, only returned arguments"
TYPE_TO_LITERAL_NO_CAST = "No cast for arguments '{0}' of '{1}' performed. Thus, neglect arguments.\nError:\n{2}"
