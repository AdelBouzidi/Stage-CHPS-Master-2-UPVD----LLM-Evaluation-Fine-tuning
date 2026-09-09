program how_many_times_demo
      implicit none
      character(len=*), dimension(1) :: string
      character(len=*), dimension(1) :: substring
      integer :: count
      integer :: pos

      ! Read input
      read(*, *) string
      read(*, *) substring

      ! Initialize count
      count = 0
      pos = 1

      ! Count occurrences
      do while (pos <= len(string) - len(substring) + 1)
        if (index(string(pos:), substring) == 1) then
          count = count + 1
          pos = pos + 1
        else
          pos = pos + 1
        end if
      end do

      ! Output result
      print *, count

    end program how_many_times_demo