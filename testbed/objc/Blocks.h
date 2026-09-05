#import <Foundation/Foundation.h>

@interface BlockPropertyExample : NSObject {
    int (^_blockProperty)(int, int);
}

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

@interface BlockObjectExample : NSObject {
    int _value;
    BlockDelegate *_delegate;
}

@property int value;
@property (retain) BlockDelegate *delegate;
- (id)initWithDelegate:(BlockDelegate *)delegate;
- (int)blockExample;
- (int)structBlockExample;
@end


@interface BlockReceiverExample : NSObject
- (int)receiverMethod:(int (^)(int, int))blockArgument;
@end


@interface BlockRoundTrip : NSObject
- (int (^)(int, int))roundTrip:(int (^)(int, int))blockArgument;
- (int (^)(void))roundTripNoArgs:(int (^)(void))blockArgument;
@end
