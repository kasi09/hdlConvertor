
GetAntlrParserFileNames("${CMAKE_CURRENT_SOURCE_DIR}" "Verilog2001" verilogParsers_GENERATED_SRC)

file(GLOB libparserVerilog_SRC
  "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

AddParserToBuild("Verilog2001" verilogParsers_GENERATED_SRC ${PARSER_GEN_ONLY_LISTENER})

set(parsersVerilog_SRC
  ${libparserVerilog_SRC}
  ${verilogParsers_GENERATED_SRC}
)

add_library(parsersVerilog_static STATIC ${parsersVerilog_SRC})
target_include_directories(
	parsersVerilog_static
	INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/Verilog2001Parser
)
add_dependencies(parsersVerilog_static generateParsersVerilog2001)
#target_link_libraries(parsersVerilog_static antlr4_shared)
set_target_properties(parsersVerilog_static
	PROPERTIES VERSION "1.0.0"
	OUTPUT_NAME parseVerilog
	POSITION_INDEPENDENT_CODE ON
)
