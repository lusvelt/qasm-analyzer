# Generated from qasm3sub.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .qasm3subParser import qasm3subParser
else:
    from qasm3subParser import qasm3subParser

# This class defines a complete listener for a parse tree produced by qasm3subParser.
class qasm3subListener(ParseTreeListener):

    # Enter a parse tree produced by qasm3subParser#program.
    def enterProgram(self, ctx:qasm3subParser.ProgramContext):
        pass

    # Exit a parse tree produced by qasm3subParser#program.
    def exitProgram(self, ctx:qasm3subParser.ProgramContext):
        pass


    # Enter a parse tree produced by qasm3subParser#header.
    def enterHeader(self, ctx:qasm3subParser.HeaderContext):
        pass

    # Exit a parse tree produced by qasm3subParser#header.
    def exitHeader(self, ctx:qasm3subParser.HeaderContext):
        pass


    # Enter a parse tree produced by qasm3subParser#version.
    def enterVersion(self, ctx:qasm3subParser.VersionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#version.
    def exitVersion(self, ctx:qasm3subParser.VersionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#include.
    def enterInclude(self, ctx:qasm3subParser.IncludeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#include.
    def exitInclude(self, ctx:qasm3subParser.IncludeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#globalStatement.
    def enterGlobalStatement(self, ctx:qasm3subParser.GlobalStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#globalStatement.
    def exitGlobalStatement(self, ctx:qasm3subParser.GlobalStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#statement.
    def enterStatement(self, ctx:qasm3subParser.StatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#statement.
    def exitStatement(self, ctx:qasm3subParser.StatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumDeclarationStatement.
    def enterQuantumDeclarationStatement(self, ctx:qasm3subParser.QuantumDeclarationStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumDeclarationStatement.
    def exitQuantumDeclarationStatement(self, ctx:qasm3subParser.QuantumDeclarationStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalDeclarationStatement.
    def enterClassicalDeclarationStatement(self, ctx:qasm3subParser.ClassicalDeclarationStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalDeclarationStatement.
    def exitClassicalDeclarationStatement(self, ctx:qasm3subParser.ClassicalDeclarationStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalAssignment.
    def enterClassicalAssignment(self, ctx:qasm3subParser.ClassicalAssignmentContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalAssignment.
    def exitClassicalAssignment(self, ctx:qasm3subParser.ClassicalAssignmentContext):
        pass


    # Enter a parse tree produced by qasm3subParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:qasm3subParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:qasm3subParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#returnSignature.
    def enterReturnSignature(self, ctx:qasm3subParser.ReturnSignatureContext):
        pass

    # Exit a parse tree produced by qasm3subParser#returnSignature.
    def exitReturnSignature(self, ctx:qasm3subParser.ReturnSignatureContext):
        pass


    # Enter a parse tree produced by qasm3subParser#designator.
    def enterDesignator(self, ctx:qasm3subParser.DesignatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#designator.
    def exitDesignator(self, ctx:qasm3subParser.DesignatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#doubleDesignator.
    def enterDoubleDesignator(self, ctx:qasm3subParser.DoubleDesignatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#doubleDesignator.
    def exitDoubleDesignator(self, ctx:qasm3subParser.DoubleDesignatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#identifierList.
    def enterIdentifierList(self, ctx:qasm3subParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#identifierList.
    def exitIdentifierList(self, ctx:qasm3subParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#association.
    def enterAssociation(self, ctx:qasm3subParser.AssociationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#association.
    def exitAssociation(self, ctx:qasm3subParser.AssociationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumType.
    def enterQuantumType(self, ctx:qasm3subParser.QuantumTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumType.
    def exitQuantumType(self, ctx:qasm3subParser.QuantumTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumDeclaration.
    def enterQuantumDeclaration(self, ctx:qasm3subParser.QuantumDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumDeclaration.
    def exitQuantumDeclaration(self, ctx:qasm3subParser.QuantumDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumArgument.
    def enterQuantumArgument(self, ctx:qasm3subParser.QuantumArgumentContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumArgument.
    def exitQuantumArgument(self, ctx:qasm3subParser.QuantumArgumentContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumArgumentList.
    def enterQuantumArgumentList(self, ctx:qasm3subParser.QuantumArgumentListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumArgumentList.
    def exitQuantumArgumentList(self, ctx:qasm3subParser.QuantumArgumentListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#bitType.
    def enterBitType(self, ctx:qasm3subParser.BitTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#bitType.
    def exitBitType(self, ctx:qasm3subParser.BitTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#singleDesignatorType.
    def enterSingleDesignatorType(self, ctx:qasm3subParser.SingleDesignatorTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#singleDesignatorType.
    def exitSingleDesignatorType(self, ctx:qasm3subParser.SingleDesignatorTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#doubleDesignatorType.
    def enterDoubleDesignatorType(self, ctx:qasm3subParser.DoubleDesignatorTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#doubleDesignatorType.
    def exitDoubleDesignatorType(self, ctx:qasm3subParser.DoubleDesignatorTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#noDesignatorType.
    def enterNoDesignatorType(self, ctx:qasm3subParser.NoDesignatorTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#noDesignatorType.
    def exitNoDesignatorType(self, ctx:qasm3subParser.NoDesignatorTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalType.
    def enterClassicalType(self, ctx:qasm3subParser.ClassicalTypeContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalType.
    def exitClassicalType(self, ctx:qasm3subParser.ClassicalTypeContext):
        pass


    # Enter a parse tree produced by qasm3subParser#constantDeclaration.
    def enterConstantDeclaration(self, ctx:qasm3subParser.ConstantDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#constantDeclaration.
    def exitConstantDeclaration(self, ctx:qasm3subParser.ConstantDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#singleDesignatorDeclaration.
    def enterSingleDesignatorDeclaration(self, ctx:qasm3subParser.SingleDesignatorDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#singleDesignatorDeclaration.
    def exitSingleDesignatorDeclaration(self, ctx:qasm3subParser.SingleDesignatorDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#doubleDesignatorDeclaration.
    def enterDoubleDesignatorDeclaration(self, ctx:qasm3subParser.DoubleDesignatorDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#doubleDesignatorDeclaration.
    def exitDoubleDesignatorDeclaration(self, ctx:qasm3subParser.DoubleDesignatorDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#noDesignatorDeclaration.
    def enterNoDesignatorDeclaration(self, ctx:qasm3subParser.NoDesignatorDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#noDesignatorDeclaration.
    def exitNoDesignatorDeclaration(self, ctx:qasm3subParser.NoDesignatorDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#bitDeclaration.
    def enterBitDeclaration(self, ctx:qasm3subParser.BitDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#bitDeclaration.
    def exitBitDeclaration(self, ctx:qasm3subParser.BitDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalDeclaration.
    def enterClassicalDeclaration(self, ctx:qasm3subParser.ClassicalDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalDeclaration.
    def exitClassicalDeclaration(self, ctx:qasm3subParser.ClassicalDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalTypeList.
    def enterClassicalTypeList(self, ctx:qasm3subParser.ClassicalTypeListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalTypeList.
    def exitClassicalTypeList(self, ctx:qasm3subParser.ClassicalTypeListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalArgument.
    def enterClassicalArgument(self, ctx:qasm3subParser.ClassicalArgumentContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalArgument.
    def exitClassicalArgument(self, ctx:qasm3subParser.ClassicalArgumentContext):
        pass


    # Enter a parse tree produced by qasm3subParser#classicalArgumentList.
    def enterClassicalArgumentList(self, ctx:qasm3subParser.ClassicalArgumentListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#classicalArgumentList.
    def exitClassicalArgumentList(self, ctx:qasm3subParser.ClassicalArgumentListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#aliasStatement.
    def enterAliasStatement(self, ctx:qasm3subParser.AliasStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#aliasStatement.
    def exitAliasStatement(self, ctx:qasm3subParser.AliasStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#indexIdentifier.
    def enterIndexIdentifier(self, ctx:qasm3subParser.IndexIdentifierContext):
        pass

    # Exit a parse tree produced by qasm3subParser#indexIdentifier.
    def exitIndexIdentifier(self, ctx:qasm3subParser.IndexIdentifierContext):
        pass


    # Enter a parse tree produced by qasm3subParser#indexIdentifierList.
    def enterIndexIdentifierList(self, ctx:qasm3subParser.IndexIdentifierListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#indexIdentifierList.
    def exitIndexIdentifierList(self, ctx:qasm3subParser.IndexIdentifierListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#indexEqualsAssignmentList.
    def enterIndexEqualsAssignmentList(self, ctx:qasm3subParser.IndexEqualsAssignmentListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#indexEqualsAssignmentList.
    def exitIndexEqualsAssignmentList(self, ctx:qasm3subParser.IndexEqualsAssignmentListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#rangeDefinition.
    def enterRangeDefinition(self, ctx:qasm3subParser.RangeDefinitionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#rangeDefinition.
    def exitRangeDefinition(self, ctx:qasm3subParser.RangeDefinitionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumGateDefinition.
    def enterQuantumGateDefinition(self, ctx:qasm3subParser.QuantumGateDefinitionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumGateDefinition.
    def exitQuantumGateDefinition(self, ctx:qasm3subParser.QuantumGateDefinitionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumGateSignature.
    def enterQuantumGateSignature(self, ctx:qasm3subParser.QuantumGateSignatureContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumGateSignature.
    def exitQuantumGateSignature(self, ctx:qasm3subParser.QuantumGateSignatureContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumBlock.
    def enterQuantumBlock(self, ctx:qasm3subParser.QuantumBlockContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumBlock.
    def exitQuantumBlock(self, ctx:qasm3subParser.QuantumBlockContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumLoop.
    def enterQuantumLoop(self, ctx:qasm3subParser.QuantumLoopContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumLoop.
    def exitQuantumLoop(self, ctx:qasm3subParser.QuantumLoopContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumLoopBlock.
    def enterQuantumLoopBlock(self, ctx:qasm3subParser.QuantumLoopBlockContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumLoopBlock.
    def exitQuantumLoopBlock(self, ctx:qasm3subParser.QuantumLoopBlockContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumStatement.
    def enterQuantumStatement(self, ctx:qasm3subParser.QuantumStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumStatement.
    def exitQuantumStatement(self, ctx:qasm3subParser.QuantumStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumInstruction.
    def enterQuantumInstruction(self, ctx:qasm3subParser.QuantumInstructionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumInstruction.
    def exitQuantumInstruction(self, ctx:qasm3subParser.QuantumInstructionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumPhase.
    def enterQuantumPhase(self, ctx:qasm3subParser.QuantumPhaseContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumPhase.
    def exitQuantumPhase(self, ctx:qasm3subParser.QuantumPhaseContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumMeasurement.
    def enterQuantumMeasurement(self, ctx:qasm3subParser.QuantumMeasurementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumMeasurement.
    def exitQuantumMeasurement(self, ctx:qasm3subParser.QuantumMeasurementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumMeasurementAssignment.
    def enterQuantumMeasurementAssignment(self, ctx:qasm3subParser.QuantumMeasurementAssignmentContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumMeasurementAssignment.
    def exitQuantumMeasurementAssignment(self, ctx:qasm3subParser.QuantumMeasurementAssignmentContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumBarrier.
    def enterQuantumBarrier(self, ctx:qasm3subParser.QuantumBarrierContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumBarrier.
    def exitQuantumBarrier(self, ctx:qasm3subParser.QuantumBarrierContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumGateModifier.
    def enterQuantumGateModifier(self, ctx:qasm3subParser.QuantumGateModifierContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumGateModifier.
    def exitQuantumGateModifier(self, ctx:qasm3subParser.QuantumGateModifierContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumGateCall.
    def enterQuantumGateCall(self, ctx:qasm3subParser.QuantumGateCallContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumGateCall.
    def exitQuantumGateCall(self, ctx:qasm3subParser.QuantumGateCallContext):
        pass


    # Enter a parse tree produced by qasm3subParser#quantumGateName.
    def enterQuantumGateName(self, ctx:qasm3subParser.QuantumGateNameContext):
        pass

    # Exit a parse tree produced by qasm3subParser#quantumGateName.
    def exitQuantumGateName(self, ctx:qasm3subParser.QuantumGateNameContext):
        pass


    # Enter a parse tree produced by qasm3subParser#unaryOperator.
    def enterUnaryOperator(self, ctx:qasm3subParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#unaryOperator.
    def exitUnaryOperator(self, ctx:qasm3subParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#relationalOperator.
    def enterRelationalOperator(self, ctx:qasm3subParser.RelationalOperatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#relationalOperator.
    def exitRelationalOperator(self, ctx:qasm3subParser.RelationalOperatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#logicalOperator.
    def enterLogicalOperator(self, ctx:qasm3subParser.LogicalOperatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#logicalOperator.
    def exitLogicalOperator(self, ctx:qasm3subParser.LogicalOperatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#expressionStatement.
    def enterExpressionStatement(self, ctx:qasm3subParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#expressionStatement.
    def exitExpressionStatement(self, ctx:qasm3subParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#expression.
    def enterExpression(self, ctx:qasm3subParser.ExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#expression.
    def exitExpression(self, ctx:qasm3subParser.ExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#xOrExpression.
    def enterXOrExpression(self, ctx:qasm3subParser.XOrExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#xOrExpression.
    def exitXOrExpression(self, ctx:qasm3subParser.XOrExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#bitAndExpression.
    def enterBitAndExpression(self, ctx:qasm3subParser.BitAndExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#bitAndExpression.
    def exitBitAndExpression(self, ctx:qasm3subParser.BitAndExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#bitShiftExpression.
    def enterBitShiftExpression(self, ctx:qasm3subParser.BitShiftExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#bitShiftExpression.
    def exitBitShiftExpression(self, ctx:qasm3subParser.BitShiftExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:qasm3subParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:qasm3subParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:qasm3subParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:qasm3subParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#unaryExpression.
    def enterUnaryExpression(self, ctx:qasm3subParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#unaryExpression.
    def exitUnaryExpression(self, ctx:qasm3subParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#expressionTerminator.
    def enterExpressionTerminator(self, ctx:qasm3subParser.ExpressionTerminatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#expressionTerminator.
    def exitExpressionTerminator(self, ctx:qasm3subParser.ExpressionTerminatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#incrementor.
    def enterIncrementor(self, ctx:qasm3subParser.IncrementorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#incrementor.
    def exitIncrementor(self, ctx:qasm3subParser.IncrementorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#builtInCall.
    def enterBuiltInCall(self, ctx:qasm3subParser.BuiltInCallContext):
        pass

    # Exit a parse tree produced by qasm3subParser#builtInCall.
    def exitBuiltInCall(self, ctx:qasm3subParser.BuiltInCallContext):
        pass


    # Enter a parse tree produced by qasm3subParser#builtInMath.
    def enterBuiltInMath(self, ctx:qasm3subParser.BuiltInMathContext):
        pass

    # Exit a parse tree produced by qasm3subParser#builtInMath.
    def exitBuiltInMath(self, ctx:qasm3subParser.BuiltInMathContext):
        pass


    # Enter a parse tree produced by qasm3subParser#castOperator.
    def enterCastOperator(self, ctx:qasm3subParser.CastOperatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#castOperator.
    def exitCastOperator(self, ctx:qasm3subParser.CastOperatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#expressionList.
    def enterExpressionList(self, ctx:qasm3subParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#expressionList.
    def exitExpressionList(self, ctx:qasm3subParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#booleanExpression.
    def enterBooleanExpression(self, ctx:qasm3subParser.BooleanExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#booleanExpression.
    def exitBooleanExpression(self, ctx:qasm3subParser.BooleanExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#comparisonExpression.
    def enterComparisonExpression(self, ctx:qasm3subParser.ComparisonExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#comparisonExpression.
    def exitComparisonExpression(self, ctx:qasm3subParser.ComparisonExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#equalsExpression.
    def enterEqualsExpression(self, ctx:qasm3subParser.EqualsExpressionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#equalsExpression.
    def exitEqualsExpression(self, ctx:qasm3subParser.EqualsExpressionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:qasm3subParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by qasm3subParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:qasm3subParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by qasm3subParser#equalsAssignmentList.
    def enterEqualsAssignmentList(self, ctx:qasm3subParser.EqualsAssignmentListContext):
        pass

    # Exit a parse tree produced by qasm3subParser#equalsAssignmentList.
    def exitEqualsAssignmentList(self, ctx:qasm3subParser.EqualsAssignmentListContext):
        pass


    # Enter a parse tree produced by qasm3subParser#membershipTest.
    def enterMembershipTest(self, ctx:qasm3subParser.MembershipTestContext):
        pass

    # Exit a parse tree produced by qasm3subParser#membershipTest.
    def exitMembershipTest(self, ctx:qasm3subParser.MembershipTestContext):
        pass


    # Enter a parse tree produced by qasm3subParser#setDeclaration.
    def enterSetDeclaration(self, ctx:qasm3subParser.SetDeclarationContext):
        pass

    # Exit a parse tree produced by qasm3subParser#setDeclaration.
    def exitSetDeclaration(self, ctx:qasm3subParser.SetDeclarationContext):
        pass


    # Enter a parse tree produced by qasm3subParser#programBlock.
    def enterProgramBlock(self, ctx:qasm3subParser.ProgramBlockContext):
        pass

    # Exit a parse tree produced by qasm3subParser#programBlock.
    def exitProgramBlock(self, ctx:qasm3subParser.ProgramBlockContext):
        pass


    # Enter a parse tree produced by qasm3subParser#branchingStatement.
    def enterBranchingStatement(self, ctx:qasm3subParser.BranchingStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#branchingStatement.
    def exitBranchingStatement(self, ctx:qasm3subParser.BranchingStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#loopSignature.
    def enterLoopSignature(self, ctx:qasm3subParser.LoopSignatureContext):
        pass

    # Exit a parse tree produced by qasm3subParser#loopSignature.
    def exitLoopSignature(self, ctx:qasm3subParser.LoopSignatureContext):
        pass


    # Enter a parse tree produced by qasm3subParser#loopStatement.
    def enterLoopStatement(self, ctx:qasm3subParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#loopStatement.
    def exitLoopStatement(self, ctx:qasm3subParser.LoopStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#controlDirectiveStatement.
    def enterControlDirectiveStatement(self, ctx:qasm3subParser.ControlDirectiveStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#controlDirectiveStatement.
    def exitControlDirectiveStatement(self, ctx:qasm3subParser.ControlDirectiveStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#controlDirective.
    def enterControlDirective(self, ctx:qasm3subParser.ControlDirectiveContext):
        pass

    # Exit a parse tree produced by qasm3subParser#controlDirective.
    def exitControlDirective(self, ctx:qasm3subParser.ControlDirectiveContext):
        pass


    # Enter a parse tree produced by qasm3subParser#subroutineDefinition.
    def enterSubroutineDefinition(self, ctx:qasm3subParser.SubroutineDefinitionContext):
        pass

    # Exit a parse tree produced by qasm3subParser#subroutineDefinition.
    def exitSubroutineDefinition(self, ctx:qasm3subParser.SubroutineDefinitionContext):
        pass


    # Enter a parse tree produced by qasm3subParser#returnStatement.
    def enterReturnStatement(self, ctx:qasm3subParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by qasm3subParser#returnStatement.
    def exitReturnStatement(self, ctx:qasm3subParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by qasm3subParser#subroutineBlock.
    def enterSubroutineBlock(self, ctx:qasm3subParser.SubroutineBlockContext):
        pass

    # Exit a parse tree produced by qasm3subParser#subroutineBlock.
    def exitSubroutineBlock(self, ctx:qasm3subParser.SubroutineBlockContext):
        pass


    # Enter a parse tree produced by qasm3subParser#subroutineCall.
    def enterSubroutineCall(self, ctx:qasm3subParser.SubroutineCallContext):
        pass

    # Exit a parse tree produced by qasm3subParser#subroutineCall.
    def exitSubroutineCall(self, ctx:qasm3subParser.SubroutineCallContext):
        pass


    # Enter a parse tree produced by qasm3subParser#pragma.
    def enterPragma(self, ctx:qasm3subParser.PragmaContext):
        pass

    # Exit a parse tree produced by qasm3subParser#pragma.
    def exitPragma(self, ctx:qasm3subParser.PragmaContext):
        pass



del qasm3subParser