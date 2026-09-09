program main
  implicit none
  integer :: n
  integer :: result

  ! Read input from stdin
  read *, n

  ! Call the function
  result = get_max_triples(n)

  ! Output the result
  print *, result

contains

  integer function get_max_triples(n)
    implicit none
    integer, intent(in) :: n
    integer :: a(n)
    integer :: i, j, k
    integer :: count

    ! Initialize array a
    do i = 1, n
      a(i) = i*i - i + 1
    end do

    ! Count triples with sum divisible by 3
    count = 0
    do i = 1, n-2
      do j = i+1, n-1
        do k = j+1, n
          if (mod(a(i) + a(j) + a(k), 3) == 0) then
            count = count + 1
          end if
        end do
      end do
    end do

    get_max_triples = count
  end function get_max_triples

end program main