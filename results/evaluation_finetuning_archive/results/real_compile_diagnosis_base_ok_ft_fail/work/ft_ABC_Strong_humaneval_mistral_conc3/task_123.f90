program get_odd_collatz_demo
  implicit none
  integer, dimension(:), allocatable :: result
  integer :: n
  
  ! Hardcoded example input
  n = 5
  
  call get_odd_collatz(n, result)
  
  print *, result
contains

  subroutine get_odd_collatz(n, result)
    integer, intent(in) :: n
    integer, intent(out), allocatable :: result(:)
    integer :: i, temp
    integer, dimension(:), allocatable :: odd_nums
    
    ! Generate Collatz sequence and collect odd numbers
    allocate(odd_nums(0))
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        allocate(odd_nums(size(odd_nums) + 1))
        odd_nums(size(odd_nums)) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    allocate(result(size(odd_nums)))
    result = odd_nums
    result = sort_array(result)
  end subroutine get_odd_collatz

  function sort_array(arr) result(sorted)
    integer, intent(in) :: arr(:)
    integer :: sorted(:)
    integer :: i, j, temp
    sorted = arr
    do i = 1, size(sorted) - 1
      do j = i + 1, size(sorted)
        if (sorted(j) < sorted(i)) then
          temp = sorted(i)
          sorted(i) = sorted(j)
          sorted(j) = temp
        end if
      end do
    end do
  end function sort_array

end program get_odd_collatz_demo