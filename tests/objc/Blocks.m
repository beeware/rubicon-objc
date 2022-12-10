#import "Blocks.h"

@implementation BlockPropertyExample

@synthesize blockProperty = _blockProperty;

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

@synthesize value = _value;
@synthesize delegate = _delegate;

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

-(int) receiverMethod:(int (^)(int, int))blockArgument
{
    return blockArgument(13, 14);
}

@end

@implementation BlockRoundTrip

- (int (^)(int, int)) roundTrip:(int (^)(int, int))blockArgument
{
    return blockArgument;
}

- (int (^)(void)) roundTripNoArgs:(int (^)(void))blockArgument
{
    return blockArgument;
}

@end
