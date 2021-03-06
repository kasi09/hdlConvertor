#include "syntaxErrorLogger.h"

void SyntaxErrorLogger::CheckErrors() {
	std::stringstream error_msg;
	error_msg << std::endl;
	for(
	std::vector<error_data>::iterator iter = _errors.begin();
	iter != _errors.end();
	iter++ ) {
		error_msg << iter->_filename 
			<< ':' << (*iter)._line
			<< ':' << (uint32_t) iter->_charPosition
		        <<  ":SyntaxError:" 
			<< iter->_message 
			<< std::endl;
	}
	if (_errors.size() > 0) {
		throw parseException(error_msg.str());	
	}

}

void SyntaxErrorLogger::syntaxError(
		Recognizer *recognizer,
		Token *offendingSymbol,
		size_t line,
		size_t charPositionInLine,
		const std::string &msg,
		std::exception_ptr e) {

	error_data data;
	data._line = line;
	data._charPosition = charPositionInLine;
	data._filename = recognizer->getInputStream()->getSourceName();
	data._message = msg;
	
	_errors.push_back(data);

	//std::cerr << line << ":" << charPositionInLine << ":Error:" << msg << "\n";
}

void SyntaxErrorLogger::reportAmbiguity(
		Parser *recognizer,
		const dfa::DFA &dfa,
		size_t startIndex,
		size_t stopIndex,
		bool exact,
		const antlrcpp::BitSet &ambigAlts,
		atn::ATNConfigSet *configs) {

}

void SyntaxErrorLogger::reportContextSensitivity(
		Parser *recognizer,
		const dfa::DFA &dfa,
		size_t startIndex,
		size_t stopIndex,
		size_t prediction,
		atn::ATNConfigSet *configs) {

}

void SyntaxErrorLogger::reportAttemptingFullContext(
		Parser *recognizer,
		const dfa::DFA &dfa,
		size_t startIndex,
		size_t stopIndex,
		const antlrcpp::BitSet &conflictingAlts,
		atn::ATNConfigSet *configs) {

}
