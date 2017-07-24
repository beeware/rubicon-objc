#import <Foundation/Foundation.h>

@interface BlockPropertyExample : NSObject
@property (copy) int (^blockProperty)(int, int);
@end


@interface BlockDelegate : NSObject
- (void)exampleMethod:(void (^)(int, int))blockArgument;
@end

@interface BlockObjectExample : NSObject
@property int value;
@property BlockDelegate *delegate;
- (id)initWithDelegate:(BlockDelegate *)delegate;
- (int)blockExample;
@end
