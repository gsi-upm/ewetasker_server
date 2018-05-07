package gojsonld

import (
	"errors"
)

var (
	LOADING_DOCUMENT_FAILED        = errors.New("loading document failed")
	LIST_OF_LISTS                  = errors.New("list of lists")
	INVALID_INDEX_VALUE            = errors.New("invalid @index value")
	CONFLICTING_INDEXES            = errors.New("conflicting indexes")
	INVALID_ID_VALUE               = errors.New("invalid @id value")
	INVALID_LOCAL_CONTEXT          = errors.New("invalid local context")
	MULTIPLE_CONTEXT_LINK_HEADERS  = errors.New("multiple context link headers")
	LOADING_REMOTE_CONTEXT_FAILED  = errors.New("loading remote context failed")
	INVALID_REMOTE_CONTEXT         = errors.New("invalid remote context")
	RECURSIVE_CONTEXT_INCLUSION    = errors.New("recursive context inclusion")
	INVALID_BASE_IRI               = errors.New("invalid base IRI")
	INVALID_VOCAB_MAPPING          = errors.New("invalid vocab mapping")
	INVALID_DEFAULT_LANGUAGE       = errors.New("invalid default language")
	KEYWORD_REDEFINITION           = errors.New("keyword redefinition")
	INVALID_TERM_DEFINITION        = errors.New("invalid term definition")
	INVALID_REVERSE_PROPERTY       = errors.New("invalid reverse property")
	INVALID_IRI_MAPPING            = errors.New("invalid IRI mapping")
	CYCLIC_IRI_MAPPING             = errors.New("cyclic IRI mapping")
	INVALID_KEYWORD_ALIAS          = errors.New("invalid keyword alias")
	INVALID_TYPE_MAPPING           = errors.New("invalid type mapping")
	INVALID_LANGUAGE_MAPPING       = errors.New("invalid language mapping")
	COLLIDING_KEYWORDS             = errors.New("colliding keywords")
	INVALID_CONTAINER_MAPPING      = errors.New("invalid container mapping")
	INVALID_TYPE_VALUE             = errors.New("invalid type value")
	INVALID_VALUE_OBJECT           = errors.New("invalid value object")
	INVALID_VALUE_OBJECT_VALUE     = errors.New("invalid value object value")
	INVALID_LANGUAGE_TAGGED_STRING = errors.New("invalid language-tagged string")
	INVALID_LANGUAGE_TAGGED_VALUE  = errors.New("invalid language-tagged value")
	INVALID_TYPED_VALUE            = errors.New("invalid typed value")
	INVALID_SET_OR_LIST_OBJECT     = errors.New("invalid set or list object")
	INVALID_LANGUAGE_MAP_VALUE     = errors.New("invalid language map value")
	COMPACTION_TO_LIST_OF_LISTS    = errors.New("compaction to list of lists")
	INVALID_REVERSE_PROPERTY_MAP   = errors.New("invalid reverse property map")
	INVALID_REVERSE_VALUE          = errors.New("invalid @reverse value")
	INVALID_REVERSE_PROPERTY_VALUE = errors.New("invalid reverse property value")

	// non spec related errors
	SYNTAX_ERROR    = errors.New("syntax error")
	NOT_IMPLEMENTED = errors.New("not implemnted")
	UNKNOWN_FORMAT  = errors.New("unknown format")
	INVALID_INPUT   = errors.New("invalid input")
	PARSE_ERROR     = errors.New("parse error")
	UNKNOWN_ERROR   = errors.New("unknown error")
)
