
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Value.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

//-----------------------------------------------------------------------------
// WpevtInst implementation
//-----------------------------------------------------------------------------
// No need to expose the internals of the pass to the outside world - keep
// everything in an anonymous namespace.
namespace {
void addInstrumentation(IRBuilder<> &builder, BasicBlock &BB){
      LLVMContext &ctx = BB.getContext();
      Type *printfArgTypes[] = {Type::getInt16PtrTy(ctx)};
      FunctionType *printfFuncType = FunctionType::get(Type::getInt32Ty(ctx), printfArgTypes, true);
      FunctionCallee printfFunc = BB.getModule()->getOrInsertFunction("printf", printfFuncType);

      Value *formatStr = builder.CreateGlobalStringPtr("%s\n");
      StringRef bbName = BB.getName();
      Value *blockNameStr = builder.CreateGlobalStringPtr(bbName);
      Value *printfArgs[] = {formatStr, blockNameStr};
      builder.CreateCall(printfFunc, printfArgs);
}

// This method implements what the pass does
void visitor(Function &F) {
    LLVMContext &ctx = F.getContext();
    StringRef functionName = F.getName();
    int blockIndex = 0;

    for (Function::iterator b = F.begin(); b != F.end(); ++b) {
        BasicBlock &BB = *b;
        std::string blockName = "#;" + functionName.str() + ";block" + std::to_string(blockIndex);
        BB.setName(blockName);
        IRBuilder<> builder(&BB);
        Instruction &entry_instr = *(BB.getFirstInsertionPt());
        builder.SetInsertPoint(&entry_instr);

        if (std::strcmp(functionName.str().c_str(), "main") != 0){
            addInstrumentation(builder, BB);
        }
        blockIndex++;
    }
}

// New PM implementation
struct WpevtInst : PassInfoMixin<WpevtInst> {
  // Main entry point, takes IR unit to run the pass on (&F) and the
  // corresponding pass manager (to be queried if need be)
  PreservedAnalyses run(Function &F, FunctionAnalysisManager &) {
    visitor(F);
    return PreservedAnalyses::none();
  }
  // Without isRequired returning true, this pass will be skipped for functions
  // decorated with the optnone LLVM attribute. Note that clang -O0 decorates
  // all functions with optnone.
  static bool isRequired() { return true; }
};

// Legacy PM implementation
struct LegacyWpevtInst : public FunctionPass {
  static char ID;
  LegacyWpevtInst() : FunctionPass(ID) {}
  // Main entry point - the name conveys what unit of IR this is to be run on.
  bool runOnFunction(Function &F) override {
    visitor(F);
    // Doesn't modify the input unit of IR, hence 'false'
    return false;
  }
};
} // namespace

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getWpevtInstPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "WpevtInst", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "wpevt-pass") {
                    FPM.addPass(WpevtInst());
                    return true;
                  }
                  return false;
                });
          }};
}

// This is the core interface for pass plugins. It guarantees that 'opt' will
// be able to recognize WpevtInst when added to the pass pipeline on the
// command line, i.e. via '-passes=wpevt-pass'
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getWpevtInstPluginInfo();
}

//-----------------------------------------------------------------------------
// Legacy PM Registration
//-----------------------------------------------------------------------------
// The address of this variable is used to uniquely identify the pass. The
// actual value doesn't matter.
char LegacyWpevtInst::ID = 0;

// This is the core interface for pass plugins. It guarantees that 'opt' will
// recognize LegacyWpevtInst when added to the pass pipeline on the command
// line, i.e.  via '--legacy-wpevt-pass'
static RegisterPass<LegacyWpevtInst>
    X("legacy-wpevt-pass", "Hello World Pass",
      true, // This pass doesn't modify the CFG => true
      false // This pass is not a pure analysis pass => false
    );