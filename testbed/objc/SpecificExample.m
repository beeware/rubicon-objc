#import "SpecificExample.h"
#import <stdio.h>

@implementation SpecificExample

-(void) method:(int) v withArg: (int) m{
    self.baseIntField = v + m;
}

-(void) methodWithArgs: (int) num, ... {

   int prod = 1;

   va_list args;
   va_start( args, num );

   for( int i = 0; i < num; i++)
   {
      prod *= va_arg( args, int);
   }

   va_end( args );

   self.baseIntField = prod;
}

@end
