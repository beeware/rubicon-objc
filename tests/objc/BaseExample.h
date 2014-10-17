#import <Foundation/Foundation.h>

@interface BaseExample : NSObject

@property int baseIntField;

+(int) staticBaseIntField;
+(void) setStaticBaseIntField: (int) v;

+(int) accessStaticBaseIntField;
+(void) mutateStaticBaseIntFieldWithValue: (int) v;

-(id) init;
-(id) initWithIntValue: (int) v;

-(int) accessBaseIntField;
-(void) mutateBaseIntFieldWithValue: (int) v;

@end
