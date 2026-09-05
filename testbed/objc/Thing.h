#import <CoreGraphics/CGGeometry.h>
#import <Foundation/Foundation.h>

@interface Thing : NSObject {
    NSString *_name;
}

@property (retain) NSString *name;

-(id) initWithName: (NSString *) name;
-(id) initWithName: (NSString *) name value: (int) v;

-(NSString *) toString;

-(CGSize) computeSize: (CGSize) input;
-(CGRect) computeRect: (CGRect) input;

@end
