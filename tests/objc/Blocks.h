#import <Foundation/Foundation.h>

@interface BlockPropertyExample : NSObject
@property (copy) int (^blockProperty)(int, int);
@end

typedef struct
{
    int a;
    int b;
} blockStruct;

@interface BlockDelegate : NSObject
- (void)exampleMethod:(void (^)(int, int))blockArgument;
- (int)structBlockMethod:(int (^)(blockStruct))blockArgument;
@end

@interface BlockObjectExample : NSObject
@property int value;
@property BlockDelegate *delegate;
- (id)initWithDelegate:(BlockDelegate *)delegate;
- (int)blockExample;
- (int)structBlockExample;
@end


@interface BlockReceiverExample : NSObject
- (void)receiverMethod:(void (^)(int, int))blockArgument;
@end