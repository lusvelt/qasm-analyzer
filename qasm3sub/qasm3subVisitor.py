# Generated from qasm3sub.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .qasm3subParser import qasm3subParser
else:
    from qasm3subParser import qasm3subParser

# This class defines a complete generic visitor for a parse tree produced by qasm3subParser.

class qasm3subVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by qasm3subParser#program.
    def visitProgram(self, ctx:qasm3subParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#header.
    def visitHeader(self, ctx:qasm3subParser.HeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#version.
    def visitVersion(self, ctx:qasm3subParser.VersionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#include.
    def visitInclude(self, ctx:qasm3subParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#globalStatement.
    def visitGlobalStatement(self, ctx:qasm3subParser.GlobalStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#statement.
    def visitStatement(self, ctx:qasm3subParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumDeclarationStatement.
    def visitQuantumDeclarationStatement(self, ctx:qasm3subParser.QuantumDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalDeclarationStatement.
    def visitClassicalDeclarationStatement(self, ctx:qasm3subParser.ClassicalDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalAssignment.
    def visitClassicalAssignment(self, ctx:qasm3subParser.ClassicalAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:qasm3subParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#returnSignature.
    def visitReturnSignature(self, ctx:qasm3subParser.ReturnSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#designator.
    def visitDesignator(self, ctx:qasm3subParser.DesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#doubleDesignator.
    def visitDoubleDesignator(self, ctx:qasm3subParser.DoubleDesignatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#identifierList.
    def visitIdentifierList(self, ctx:qasm3subParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#association.
    def visitAssociation(self, ctx:qasm3subParser.AssociationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumType.
    def visitQuantumType(self, ctx:qasm3subParser.QuantumTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumDeclaration.
    def visitQuantumDeclaration(self, ctx:qasm3subParser.QuantumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumArgument.
    def visitQuantumArgument(self, ctx:qasm3subParser.QuantumArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumArgumentList.
    def visitQuantumArgumentList(self, ctx:qasm3subParser.QuantumArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#bitType.
    def visitBitType(self, ctx:qasm3subParser.BitTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#singleDesignatorType.
    def visitSingleDesignatorType(self, ctx:qasm3subParser.SingleDesignatorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#doubleDesignatorType.
    def visitDoubleDesignatorType(self, ctx:qasm3subParser.DoubleDesignatorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#noDesignatorType.
    def visitNoDesignatorType(self, ctx:qasm3subParser.NoDesignatorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalType.
    def visitClassicalType(self, ctx:qasm3subParser.ClassicalTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#constantDeclaration.
    def visitConstantDeclaration(self, ctx:qasm3subParser.ConstantDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#singleDesignatorDeclaration.
    def visitSingleDesignatorDeclaration(self, ctx:qasm3subParser.SingleDesignatorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#doubleDesignatorDeclaration.
    def visitDoubleDesignatorDeclaration(self, ctx:qasm3subParser.DoubleDesignatorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#noDesignatorDeclaration.
    def visitNoDesignatorDeclaration(self, ctx:qasm3subParser.NoDesignatorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#bitDeclaration.
    def visitBitDeclaration(self, ctx:qasm3subParser.BitDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalDeclaration.
    def visitClassicalDeclaration(self, ctx:qasm3subParser.ClassicalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalTypeList.
    def visitClassicalTypeList(self, ctx:qasm3subParser.ClassicalTypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalArgument.
    def visitClassicalArgument(self, ctx:qasm3subParser.ClassicalArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#classicalArgumentList.
    def visitClassicalArgumentList(self, ctx:qasm3subParser.ClassicalArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#aliasStatement.
    def visitAliasStatement(self, ctx:qasm3subParser.AliasStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#indexIdentifier.
    def visitIndexIdentifier(self, ctx:qasm3subParser.IndexIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#indexIdentifierList.
    def visitIndexIdentifierList(self, ctx:qasm3subParser.IndexIdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#indexEqualsAssignmentList.
    def visitIndexEqualsAssignmentList(self, ctx:qasm3subParser.IndexEqualsAssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#rangeDefinition.
    def visitRangeDefinition(self, ctx:qasm3subParser.RangeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumGateDefinition.
    def visitQuantumGateDefinition(self, ctx:qasm3subParser.QuantumGateDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumGateSignature.
    def visitQuantumGateSignature(self, ctx:qasm3subParser.QuantumGateSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumBlock.
    def visitQuantumBlock(self, ctx:qasm3subParser.QuantumBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumLoop.
    def visitQuantumLoop(self, ctx:qasm3subParser.QuantumLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumLoopBlock.
    def visitQuantumLoopBlock(self, ctx:qasm3subParser.QuantumLoopBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumStatement.
    def visitQuantumStatement(self, ctx:qasm3subParser.QuantumStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumInstruction.
    def visitQuantumInstruction(self, ctx:qasm3subParser.QuantumInstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumPhase.
    def visitQuantumPhase(self, ctx:qasm3subParser.QuantumPhaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumMeasurement.
    def visitQuantumMeasurement(self, ctx:qasm3subParser.QuantumMeasurementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumMeasurementAssignment.
    def visitQuantumMeasurementAssignment(self, ctx:qasm3subParser.QuantumMeasurementAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumBarrier.
    def visitQuantumBarrier(self, ctx:qasm3subParser.QuantumBarrierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumGateModifier.
    def visitQuantumGateModifier(self, ctx:qasm3subParser.QuantumGateModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumGateCall.
    def visitQuantumGateCall(self, ctx:qasm3subParser.QuantumGateCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#quantumGateName.
    def visitQuantumGateName(self, ctx:qasm3subParser.QuantumGateNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#unaryOperator.
    def visitUnaryOperator(self, ctx:qasm3subParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#relationalOperator.
    def visitRelationalOperator(self, ctx:qasm3subParser.RelationalOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#logicalOperator.
    def visitLogicalOperator(self, ctx:qasm3subParser.LogicalOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#expressionStatement.
    def visitExpressionStatement(self, ctx:qasm3subParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#expression.
    def visitExpression(self, ctx:qasm3subParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#xOrExpression.
    def visitXOrExpression(self, ctx:qasm3subParser.XOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#bitAndExpression.
    def visitBitAndExpression(self, ctx:qasm3subParser.BitAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#bitShiftExpression.
    def visitBitShiftExpression(self, ctx:qasm3subParser.BitShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:qasm3subParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:qasm3subParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#unaryExpression.
    def visitUnaryExpression(self, ctx:qasm3subParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#expressionTerminator.
    def visitExpressionTerminator(self, ctx:qasm3subParser.ExpressionTerminatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#incrementor.
    def visitIncrementor(self, ctx:qasm3subParser.IncrementorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#builtInCall.
    def visitBuiltInCall(self, ctx:qasm3subParser.BuiltInCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#builtInMath.
    def visitBuiltInMath(self, ctx:qasm3subParser.BuiltInMathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#castOperator.
    def visitCastOperator(self, ctx:qasm3subParser.CastOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#expressionList.
    def visitExpressionList(self, ctx:qasm3subParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#booleanExpression.
    def visitBooleanExpression(self, ctx:qasm3subParser.BooleanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:qasm3subParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#equalsExpression.
    def visitEqualsExpression(self, ctx:qasm3subParser.EqualsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:qasm3subParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#equalsAssignmentList.
    def visitEqualsAssignmentList(self, ctx:qasm3subParser.EqualsAssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#membershipTest.
    def visitMembershipTest(self, ctx:qasm3subParser.MembershipTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#setDeclaration.
    def visitSetDeclaration(self, ctx:qasm3subParser.SetDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#programBlock.
    def visitProgramBlock(self, ctx:qasm3subParser.ProgramBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#branchingStatement.
    def visitBranchingStatement(self, ctx:qasm3subParser.BranchingStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#loopSignature.
    def visitLoopSignature(self, ctx:qasm3subParser.LoopSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#loopStatement.
    def visitLoopStatement(self, ctx:qasm3subParser.LoopStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#controlDirectiveStatement.
    def visitControlDirectiveStatement(self, ctx:qasm3subParser.ControlDirectiveStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#controlDirective.
    def visitControlDirective(self, ctx:qasm3subParser.ControlDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#subroutineDefinition.
    def visitSubroutineDefinition(self, ctx:qasm3subParser.SubroutineDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#returnStatement.
    def visitReturnStatement(self, ctx:qasm3subParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#subroutineBlock.
    def visitSubroutineBlock(self, ctx:qasm3subParser.SubroutineBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#subroutineCall.
    def visitSubroutineCall(self, ctx:qasm3subParser.SubroutineCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qasm3subParser#pragma.
    def visitPragma(self, ctx:qasm3subParser.PragmaContext):
        return self.visitChildren(ctx)



del qasm3subParser