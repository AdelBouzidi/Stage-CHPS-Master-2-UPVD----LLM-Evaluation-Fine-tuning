program main
          use tuple_mod
          implicit none
          integer :: input_num
          type(tuple) :: result

          read(*, *) input_num
          result = even_odd_count(input_num)
          print *, result%val1, result%val2
        end program main