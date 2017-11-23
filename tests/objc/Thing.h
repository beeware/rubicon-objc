#import <Foundation/Foundation.h>

@interface Thing : NSObject {
    NSString *_name;
}

@property (retain) NSString *name;

-(id) initWithName: (NSString *) name;
-(id) initWithName: (NSString *) name value: (int) v;

-(NSString *) toString;

-(NSSize) computeSize: (NSSize) input;
-(NSRect) computeRect: (NSRect) input;

@end
