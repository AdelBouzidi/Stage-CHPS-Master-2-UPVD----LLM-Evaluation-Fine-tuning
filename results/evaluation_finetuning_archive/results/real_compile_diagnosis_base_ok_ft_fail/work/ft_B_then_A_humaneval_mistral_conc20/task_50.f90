program main
      implicit none
      character(len=*), dimension(:), allocatable :: s
      character(len=*), dimension(:), allocatable :: result

      read(*,*) s
      result = decode_shift(s)
      print *, result
    end program main