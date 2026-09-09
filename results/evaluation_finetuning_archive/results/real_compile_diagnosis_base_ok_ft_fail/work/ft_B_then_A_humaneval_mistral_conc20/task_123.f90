program collatz_odd
      implicit none
      integer :: n
      integer, allocatable :: result(:)

      read *, n
      result = get_odd_collatz(n)
      write (*, '(100i0)') result

    contains

      function get_odd_collatz(n) result(arr)
        implicit none
        integer, intent(in) :: n
        integer, allocatable :: arr(:)
        integer :: i, temp, size
        integer, allocatable :: temp_arr(:)

        size = 0
        i = n
        do while (i /= 1)
          if (mod(i, 2) /= 0) then
            size = size + 1
          end if
          if (mod(i, 2) == 0) then
            i = i / 2
          else
            i = 3 * i + 1
          end if
        end do
        if (mod(n, 2) /= 0) then
          size = size + 1
        end if

        allocate(arr(size))
        i = 1
        temp = n
        do while (temp /= 1)
          if (mod(temp, 2) /= 0) then
            arr(i) = temp
            i = i + 1
          end if
          if (mod(temp, 2) == 0) then
            temp = temp / 2
          else
            temp = 3 * temp + 1
          end if
        end do
        if (mod(temp, 2) /= 0) then
          arr(i) = temp
          i = i + 1
        end if

        call sort_array(arr)

      end function get_odd_collatz

      subroutine sort_array(arr)
        implicit none
        integer, intent(inout) :: arr(:)
        integer :: i, j, temp
        do i = 1, size(arr) - 1
          do j = i + 1, size(arr)
            if (arr(j) < arr(i)) then
              temp = arr(i)
              arr(i) = arr(j)
              arr(j) = temp
            end if
          end do
        end do
      end subroutine sort_array

    end program collatz_odd