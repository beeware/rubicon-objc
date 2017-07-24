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

-(int) blockExample {
    BlockDelegate *delegate = self.delegate;
    NSLog(@"Delegate is: %@", delegate);

    [delegate exampleMethod:^(int a, int b){
        self.value = a + b;
    }];
    return self.value;
}
@end
