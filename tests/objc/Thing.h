#import <Foundation/Foundation.h>

@interface Thing : NSObject {
    NSString *_name;
}

@property (retain) NSString *name;

-(id) initWithName: (NSString *) name;
-(id) initWithName: (NSString *) name value: (int) v;

-(NSString *) toString;

@end
