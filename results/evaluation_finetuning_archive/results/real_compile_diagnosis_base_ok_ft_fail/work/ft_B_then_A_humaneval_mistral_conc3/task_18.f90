program how_many_times_demo
      implicit none
      character(len=:), allocatable :: string, substring
      integer :: count, pos, len_str, len_sub

      ! Read input
      read(*, *) string
      read(*, *) substring

      ! Initialize
      count = 0
      len_str = len(string)
      len_sub = len(substring)

      ! Count occurrences
      pos = 1
      do while (pos <= len_str - len_sub + 1)
        if (string(pos:pos+len_sub-1) == substring) then
          count = count + 1
        end if
        pos = pos + 1
      end do

      ! Output
      print *, count
    end program how_many_times_demo