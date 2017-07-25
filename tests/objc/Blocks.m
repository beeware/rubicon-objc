#import "Blocks.h"

@implementation BlockPropertyExample

-(id) init
{
    self = [super init];

    if (self) {
        self.blockProperty = ^(int a, int b){
            return a + b;
        };
    }
    return self;
}

@end

@implementation BlockObjectExample

-(id) initWithDelegate:(BlockDelegate *)delegate
{
    self = [super init];
    if (self) {
        self.delegate = delegate;
    }
    return self;
}

-(int) blockExample
{
    BlockDelegate *delegate = self.delegate;

    [delegate exampleMethod:^(int a, int b){
        self.value = a + b;
    }];
    return self.value;
}

-(int) structBlockExample
{
    BlockDelegate *delegate = self.delegate;
    return [delegate structBlockMethod:^(blockStruct bs){
        return bs.a + bs.b;
    }];
}
@end

@implementation BlockReceiverExample

-(void) receiverMethod:(void (^)(int, int))blockArgument
{
    blockArgument(13, 14);
}

@end